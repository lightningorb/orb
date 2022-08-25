# @Author: w
# @Date:   2022-08-10 10:50:05
# @Last Modified by:   w
# @Last Modified time: 2022-08-10 11:00:52

for f in third_party/*; do
    if $(test -d $f); then
        echo $f;
        export PYTHONPATH="${f}:${PYTHONPATH}"
    fi
done

export PYTHONPATH="orb/lnd/grpc_generated/v0_15_0_beta/:${PYTHONPATH}"