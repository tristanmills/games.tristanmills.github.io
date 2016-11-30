var systemImages = [
	'/img/systems/arcade.png',
	'/img/systems/atari-2600.png',
	'/img/systems/atari-7800.png',
	'/img/systems/atari-lynx.png',
	'/img/systems/nintendo-game-boy-advance.png',
	'/img/systems/nintendo-game-boy-color.png',
	'/img/systems/nintendo-game-boy.png',
	'/img/systems/neo-geo-pocket-color.png',
	'/img/systems/neo-geo-pocket.png',
	'/img/systems/neo-geo.png',
	'/img/systems/nintendo-64.png',
	'/img/systems/nintendo-entertainment-system-nes.png',
	'/img/systems/sony-playstation.png',
	'/img/systems/sega-32x.png',
	'/img/systems/sega-cd.png',
	'/img/systems/sega-game-gear.png',
	'/img/systems/sega-genesis.png',
	'/img/systems/sega-master-system.png',
	'/img/systems/sega-sg-1000.png',
	'/img/systems/super-nintendo-snes.png',
	'/img/systems/turbografx-16.png',
	'/img/systems/nintendo-virtual-boy.png',
];

function preloadImages(images) {

	for (var i = 0; i < images.length; i++) {

		$('<img />').attr('src', images[i]);

	}

}

jQuery(document).ready(function($) {

	preloadImages(systemImages);

	$.getJSON('partial-metadata.json', function(metadata) {

		metadata = Metadata.filterMetadata(metadata);

		var html = Metadata.renderMetadata(metadata);

		$('#games').html(html);

		$('.filter').on('click', metadata, function(event) {

			var metadata = event.data;

			var filters = [];

			event.preventDefault();

			$(this).toggleClass('active');

			$(this).blur();

			$('.filter.active').each(function() {

				filters.push($(this).attr('id').replace('filter-', ''));

			});

			metadata = Metadata.filterMetadata(metadata, filters);

			var html = Metadata.renderMetadata(metadata);

			$('#games').html(html);

		});

	});

});