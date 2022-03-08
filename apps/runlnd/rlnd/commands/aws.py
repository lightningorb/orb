import os
from time import sleep
from invoke import task
from fabric import Connection
from textwrap import dedent
from .prefs import get_key_path
import socket

try:
    import boto3
    from botocore.exceptions import ClientError

    client = boto3.client("ec2")
    ec2 = boto3.resource("ec2")
except:
    # not using aws
    pass


@task
def save_credentials(c, key_id: str, access_key: str, region: str):
    """
    Saves your AWS credentials and default zone in your
    default AWS configuration files:

    ~/.aws/config
    ~/.aws/credentials
    """
    config = dedent(
        f"""
        [default]
        region = {region}
        """
    )
    cred = dedent(
        f"""
        [default]
        aws_access_key_id = {key_id}
        aws_secret_access_key = {access_key}
        """
    )
    aws_dir = os.path.expanduser("~/.aws")
    config_file_path = os.path.expanduser("~/.aws/config")
    credentials_file_path = os.path.expanduser("~/.aws/credentials")
    if not os.path.isdir(aws_dir):
        os.mkdir(aws_dir)
    with open(config_file_path, "w") as f:
        f.write(config)
    with open(credentials_file_path, "w") as f:
        f.write(cred)


def get_public_ip(instance_id):
    """
    Return the public ip address for given instance
    """
    for reservation in client.describe_instances(InstanceIds=[instance_id]).get(
        "Reservations"
    ):
        for instance in reservation["Instances"]:
            return instance.get("PublicIpAddress")


def get_instance(name):
    """
    Return the aws instance for the given instance name
    """
    instances = ec2.instances.filter(
        Filters=[
            {"Name": "tag:Name", "Values": [name]},
            {"Name": "instance-state-name", "Values": ["running"]},
        ]
    )
    return next(iter(instances), None)


@task(help=dict(name="The EC2 instance name you chose during creation"))
def show_ip(c, name):
    """
    Print and return the public ip address for the given
    AWS instance name
    """
    ip = get_instance(name=name).public_ip_address
    print(ip)
    return ip


@task(help=dict(name="The EC2 key-pair to ssh into this node"))
def create_keypair(c, name):
    """
    Create a key-pair called 'name' in default AWS region
    """
    response = ec2.create_key_pair(KeyName=name)
    with open(get_key_path(name), "w") as file:
        file.write(response.key_material)
    os.chmod(get_key_path(name), 0o400)


@task(help=dict(name="The EC2 key-pair to delete"))
def delete_keypair(c, name):
    """
    Delete a key-pair called 'name' in the default AWS region
    """
    response = client.delete_key_pair(KeyName=name)
    print("deleted keypair")
    print(response)


@task
def describe_key_pairs(c):
    """
    Print and retrieve all key-pairs for default AWS region
    """
    response = client.describe_key_pairs()
    print(response)
    return response


@task
def create_security_group(c):
    """
    Create the 'lightning' security group. This is the AWS EC2 level
    firewall protection that prevents the outside world from connecting
    to your node. Please note this is created in your default region.
    """
    response = client.describe_vpcs()
    vpc_id = response.get("Vpcs", [{}])[0].get("VpcId", "")

    try:
        response = client.create_security_group(
            GroupName="lightning",
            Description="security group for my lightning node",
            VpcId=vpc_id,
        )
        security_group_id = response["GroupId"]
        print("Security Group Created %s in vpc %s." % (security_group_id, vpc_id))

        data = client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": pr,
                    "FromPort": p,
                    "ToPort": p,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                }
                for p, pr in [
                    (22, "tcp"),  # SSH
                    (10009, "tcp"),  # standard GRPC
                    (9735, "tcp"),  # standard P2P
                    (9911, "tcp"),  # watch-tower
                    (60001, "udp"),  # mosh
                    (60002, "udp"),  # mosh
                    (60003, "udp"),  # mosh
                ]
            ],
        )
        print("Ingress Successfully Set %s" % data)
    except ClientError as e:
        print(e)


amis = {
    "ap-southeast-1": "ami-0d058fe428540cd89",
    "us-east-1": "ami-09e67e426f25ce0d7",
    "us-east-2": "ami-0277b52859bac6f4b",
    "us-west-1": "ami-02f24ad9a1d24a799",
    "us-west-2": "ami-03d5c68bab01f3496",
    "af-south-1": "ami-08a4b40f2fe1e4b35",
    "ap-east-1": "ami-0b215afe809665ae5",
    "ap-south-1": "ami-011c99152163a87ae",
    "ap-northeast-3": "ami-0001d1dd884af8872",
    "ap-northeast-2": "ami-04876f29fd3a5e8ba",
    "ap-northeast-1": "ami-0df99b3a8349462c6",
    "ap-southeast-2": "ami-0567f647e75c7bc05",
    "ca-central-1": "ami-0801628222e2e96d6",
    "eu-central-1": "ami-05f7491af5eef733a",
    "eu-west-1": "ami-0f89681a05a3a9de7",
    "eu-west-2": "ami-0194c3e07668a7e36",
    "eu-west-3": "ami-0f7cd40eac2214b37",
    "eu-south-1": "ami-018f430e4f5375e69",
    "eu-north-1": "ami-0ff338189efb7ed37",
    "me-south-1": "ami-0eddb8cfbd6a5f657",
    "sa-east-1": "ami-054a31f1b3bf90920",
}


@task(
    help=dict(
        instance_type="EC2 instance type, recommended: t3.medium",
        availability_zone="Exact zone, e.g if you're using us-east-1 as your default zone, this has to be e.g us-east-1a",
        name="EC2 instances have names, a good name would be mainnet",
    )
)
def create(c, instance_type: str, availability_zone: str, keypair_name: str, name: str):
    """
    Create the AWS EC2 instance, and wait until it's running, has a public
    IP, and we're able to SSH into it.
    """
    print("Creating instance...")
    ami = next(iter([amis[x] for x in amis if x in availability_zone]))
    print(f"found AMI: {ami}")
    inst = ec2.create_instances(
        Placement={"AvailabilityZone": availability_zone},
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": name},
                ],
            },
        ],
        ImageId=ami,
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 25,
                    "VolumeType": "io2",
                    "Iops": 200,
                    "Encrypted": True,
                },
            },
        ],
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=keypair_name,
        SecurityGroupIds=[
            "lightning",
        ],
    )[0]

    print("waiting until running..")
    inst.wait_until_running()

    while True:
        ip = get_public_ip(inst.id)
        if ip:
            print(ip)
            break
        print("waiting for ip address")
        sleep(5)

    print(f"ip address: {ip}")

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, 22))
        if result == 0:
            print("Instance is UP & accessible on port 22, the IP address is:  ", ip)
            break
        else:
            print("instance is still down retrying...")
            sleep(5)

    connection = Connection(
        ip, connect_kwargs={"key_filename": get_key_path(name)}, user="ubuntu"
    )

    while True:
        try:
            connection.run("whoami")
            break
        except:
            print("Cannot SSH.. let's wait")
            sleep(5)

    print(f"Created instance: {inst.id}, {ip}")
    sleep(10)
    return ip


@task(
    help=dict(
        disk_size="The disk's size in GB",
        availability_zone="The exact zone in which to create the disk. This is usually your default zone adding with an a or b.",
        name="The name of the newly created disk",
    )
)
def create_blockchain_disk(c, disk_size: str, availability_zone: str, name: str):
    """
    Create the blockchain disk of the given size, name, and in given availability zone.
    """
    print(
        f"Creating blockchain disk of size {disk_size}, in {availability_zone} named {name}"
    )
    response = ec2.create_volume(
        AvailabilityZone=availability_zone,
        VolumeType="gp3",
        TagSpecifications=[
            {
                "ResourceType": "volume",
                "Tags": [
                    {"Key": "Name", "Value": name},
                ],
            },
        ],
        Encrypted=False,
        Iops=100,
        Size=int(disk_size),
    )
    print(response.id)
    client.get_waiter("volume_available").wait(VolumeIds=[response.id])
    print("***Success!! volume:", response.id, "created...")


@task(help=dict(disk_name="The disk's name", node_name="The node's name"))
def attach_blockchain_disk(c, disk_name: str, node_name: str):
    """
    Attach disk to the node.
    """
    volume = next(
        iter(ec2.volumes.filter(Filters=[{"Name": "tag:Name", "Values": [disk_name]}])),
        None,
    )
    instance = get_instance(node_name)
    client.attach_volume(Device="/dev/sdd", InstanceId=instance.id, VolumeId=volume.id)
    client.get_waiter("volume_in_use").wait(VolumeIds=[volume.id])
    print("***Success!! volume:", volume.id, "attached...")


@task(help=dict(disk_name="The disk's name"))
def delete_blockchain_disk(c, disk_name: str):
    """
    Delete disk with the given name. User with care.
    """
    volume = next(
        iter(ec2.volumes.filter(Filters=[{"Name": "tag:Name", "Values": [disk_name]}])),
        None,
    )
    response = client.delete_volume(VolumeId=volume.id)
    print(response)


@task(help=dict(disk_name="The disk's name"))
def detach_blockchain_disk(c, disk_name: str):
    """
    Detach disk with the given name.
    """
    volume = next(
        iter(ec2.volumes.filter(Filters=[{"Name": "tag:Name", "Values": [disk_name]}])),
        None,
    )
    try:
        response = client.detach_volume(VolumeId=volume.id, Force=True)
        print(response)
        # todo: wait properly, not by just sleeping
        sleep(60)
    except:
        print("exception.. continuing")


@task(
    help=dict(
        disk_size="The disk's size in GB.", format="Whether to format the disk or not"
    )
)
def config_blockchain_disk(c, disk_size: int, format: bool = False):
    """
    Add the disk to fstab, mount it, format it (optional), and create the /blockchain fs path.
    """
    while True:
        disk = c.sudo(
            "lsblk | grep " + str(disk_size) + "G | awk '{print $1}'"
        ).stdout.strip()
        if disk:
            break
        else:
            print("couldn't find disk - waiting")
            sleep(5)
    print(c.sudo(f"file -s /dev/{disk}"))
    if format:
        c.sudo(f"mkfs -t ext4 /dev/{disk}")
    c.sudo("mkdir -p /blockchain")
    c.sudo(f"mount /dev/{disk} /blockchain/")
    c.sudo("df -h /blockchain")
    c.sudo(
        f"echo '/dev/{disk} /blockchain ext4 defaults,nofail 0 0' | sudo tee -a /etc/fstab"
    )
    c.sudo("mount -a")
    c.sudo("chown ubuntu /blockchain")


@task()
def kill(c, node_name: str, force: bool = False):
    """
    Delete the node.
    """
    instance = get_instance(name=node_name)
    if not instance:
        print(f"no instance {node_name} found")
        exit()
    if force or "y" in input(f"kill instance {node_name}? y/n: "):
        client.stop_instances(InstanceIds=[instance.id])
        client.terminate_instances(InstanceIds=[instance.id])
        print(f"Stopped instance: {instance.id}")
        print(f"Terminated instance: {instance.id}")


@task
def show_running(c):
    """
    Print out a list of running instances, and their ip addresses
    """
    for inst in ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    ):
        for tag in inst.tags:
            if "Name" in tag["Key"]:
                print(tag["Value"], inst.public_ip_address)
