function filterGames(games, filters) {

	var games = jQuery.extend(true, [], games);

	var ignored = [
		'Amstrad CPC',
		'Famicom Disk System',
		'Final Burn Alpha',
		'MAME',
		'MSX / MSX2',
		'Vectrex',
		'ZX Spectrum',
	];

	for (system in games) {

		if (ignored.indexOf(system) != -1) {
			delete games[system];
			continue;
		}

		games[system].forEach(function(game, index) {

			if (filters.indexOf('multiplayer') != -1 && game.players < 2) {
				delete games[system][index];
			} else if (filters.indexOf('simultaneous-coop') != -1 && game.multiplayer['simultaneous-coop'] !== true) {
				delete games[system][index];
			} else if (filters.indexOf('alternating-coop') != -1 && game.multiplayer['alternating-coop'] !== true) {
				delete games[system][index];
			} else if (filters.indexOf('simultaneous-vs') != -1 && game.multiplayer['simultaneous-vs'] !== true) {
				delete games[system][index];
			} else if (filters.indexOf('alternating-vs') != -1 && game.multiplayer['alternating-vs'] !== true) {
				delete games[system][index];
			}

		});

		games[system] = games[system].filter(function(){return true;});

	}

	return games;

}

function renderGames(games) {

	$('#games').empty();

	for (system in games) {

		var system_heading = system.replace(/\s+/g, '-').toLowerCase();
		var system_content = system_heading + '-games';

		var html = '';

		html += '<h5 id="' + system_heading + '">';
			html += '<a data-toggle="collapse" data-parent="#games" href="#' + system_content + '" aria-controls="' + system_content + '">';
				html += '<img class="system-icon" src="/img/' + system_heading + '.png">';
				html += '<span>' + system + ' (' + games[system].length + ')</span>';
			html += '</a>';
		html += '</h5>';

		html += '<ul id="' + system_content + '" class="collapse" role="tabpanel" aria-labelledby="' + system_heading + '">';

		games[system].forEach(function(game) {

			var compatibility = '';
			var multiplayer = '';
			var simultaneous_coop = '';
			var simultaneous_vs = '';
			var alternating_coop = '';
			var alternating_vs = '';

			if (game.compatibility['pi3'] === true) {
				compatibility = ' class="pass"';
			} else if (game.compatibility['pi3'] === false) {
				compatibility = ' class="fail"';
			}

			if (game.players > 1) {
				multiplayer = ' <span class="tag tag-info">Multi (' + game.players + ')</span>';
			}

			if (game.multiplayer['simultaneous-coop']) {
				simultaneous_coop = ' <span class="tag tag-success">Simo Co-Op</span>';
			}

			if (game.multiplayer['alternating-coop']) {
				alternating_coop = ' <span class="tag tag-success">Alt Co-Op</span>';
			}

			if (game.multiplayer['simultaneous-vs']) {
				simultaneous_vs = ' <span class="tag tag-danger">Simo Vs</span>';
			}

			if (game.multiplayer['alternating-vs']) {
				alternating_vs = ' <span class="tag tag-danger">Alt Vs</span>';
			}

			html += '<li' + compatibility + '>' + game.name + multiplayer + simultaneous_coop + alternating_coop + simultaneous_vs + alternating_vs + '</li>';

		});

		if (games[system].length === 0) {
			html += '<li>None</li>';
		}

		html += '</ul>';

		$('#games').append(html);

	}

}

jQuery(document).ready(function($) {

	$.getJSON('games.json', function(games) {

		var filtered_games = filterGames(games, []);

		renderGames(filtered_games);

		$('.filter').on('click', function(event) {

			event.preventDefault();

			$(this).toggleClass('active');

			$(this).blur();

			var filters = [];

			$('.filter.active').each(function() {
				filters.push($(this).attr('id'));
			});

			filtered_games = filterGames(games, filters);

			renderGames(filtered_games);

		});

	});

});