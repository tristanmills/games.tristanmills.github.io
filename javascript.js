function filterGames(games, filters) {

	var games = jQuery.extend(true, [], games);

	for (system in games) {

		games[system].forEach(function(game, index) {

			if (filters.indexOf('multiplayer') != -1 && game.players < 2) {
				delete games[system][index];
			} else if (filters.indexOf('simultaneous-coop') != -1 && game.multiplayer['simultaneous-coop'] === false) {
				delete games[system][index];
			} else if (filters.indexOf('alternating-coop') != -1 && game.multiplayer['alternating-coop'] === false) {
				delete games[system][index];
			} else if (filters.indexOf('simultaneous-vs') != -1 && game.multiplayer['simultaneous-vs'] === false) {
				delete games[system][index];
			} else if (filters.indexOf('alternating-vs') != -1 && game.multiplayer['alternating-vs'] === false) {
				delete games[system][index];
			}

		});

		games[system] = games[system].filter(function(){return true;});

		if (games[system].length === 0) {
			games[system].push({
				'name': 'None',
				'multiplayer': {}
			})
		}
	}

	return games;

}

function renderGames(games) {

	$('#games').empty();

	for (system in games) {

		var html = '<h3>' + system + '</h3>';

		html += '<ul>';

		games[system].forEach(function(game) {

			var tested = '';
			var multiplayer = '';
			var simultaneous_coop = '';
			var simultaneous_vs = '';
			var alternating_coop = '';
			var alternating_vs = '';

			if (game.tested) {
				tested = ' class="checked"';
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

			html += '<li' + tested + '>' + game.name + multiplayer + simultaneous_coop + alternating_coop + simultaneous_vs + alternating_vs + '</li>';

		});

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