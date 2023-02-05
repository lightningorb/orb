<script>
	const toggleSwitcher = () => {
		var i = document.getElementById('style-switcher');
		if (i.style.left === '-189px') {
			i.style.left = '0px';
		} else {
			i.style.left = '-189px';
		}
	};
	function setColor(el) {
		document.getElementById('color-opt').href = '/css/colors/' + el + '.css';
	}
</script>

<div id="style-switcher" on:click={toggleSwitcher} style="left: -189px">
	<div>
		<h3>Select your color</h3>
		<ul class="pattern">
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color1" href={'#'} on:click|preventDefault={() => setColor('cyan')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color2" href={'#'} on:click|preventDefault={() => setColor('red')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color3" href={'#'} on:click|preventDefault={() => setColor('green')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color4" href={'#'} on:click|preventDefault={() => setColor('pink')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color5" href={'#'} on:click|preventDefault={() => setColor('blue')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color6" href={'#'} on:click|preventDefault={() => setColor('purple')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color7" href={'#'} on:click|preventDefault={() => setColor('orange')} />
			</li>
			<li>
				<!-- svelte-ignore a11y-missing-content -->
				<a class="color8" href={'#'} on:click|preventDefault={() => setColor('yellow')} />
			</li>
		</ul>
	</div>
	<div class="bottom">
		<a href={'#'} class="settings rounded-right"><i class="mdi mdi-settings mdi-spin" /></a>
	</div>
</div>
