<!-- 
    let email = '';
    let statusMessage = '';

    async function submitEmail() {
        try {
            const response = await fetch('https://4wuzfpyv54z7tykr5jo6nw2cfy0kfhog.lambda-url.us-east-2.on.aws/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            if (response.ok) {
                console.log(await response.json());
                statusMessage = 'Thank you! Your interest has been registered.';
            } else {
                statusMessage = 'Oops! Something went wrong. Please try again later.';
            }
            console.log(response);
        } catch (error) {
            console.error('Error submitting email:', error);
            statusMessage = 'Oops! Something went wrong. Please try again later.';
        }
    } -->

<!--     <form on:submit|preventDefault={submitEmail}>
        <div class="input-group mb-3">
            <Input type="email" class="form-control" placeholder="Your Email Address" aria-label="Your Email Address" aria-describedby="basic-addon2" bind:value={email} required />
            <div class="input-group-append">
                <Button class="btn btn-primary" on:click|once={submitEmail}>Register Interest</Button>
            </div>
        </div>
    </form>
    {#if statusMessage}
        <p class="pt-3 text-black mx-auto">
            {statusMessage}
        </p>
    {/if} -->