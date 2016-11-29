var Metadata = (function() {

	'use strict';

	var ignoredSystems = [
		'Amstrad CPC',
		'Famicom Disk System',
		'Final Burn Alpha',
		'MAME',
		'MSX / MSX2',
		'Vectrex',
		'ZX Spectrum',
	];

	var filterMetadata = function(metadata, filters) {

		metadata = jQuery.extend(true, [], metadata);

		filters = typeof filters !== 'undefined' ? filters : [];

		metadata.forEach(function(system, systemIndex) {

			if (ignoredSystems.indexOf(system.name) != -1) {
				delete metadata[systemIndex];
				return;
			}

			system.games.forEach(function(game, gameIndex) {

				if (filters.indexOf('pi3') != -1 && game.compatibility.pi3 !== true) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('pi0') != -1 && game.compatibility.pi0 !== true) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('multiplayer') != -1 && game.players < 2) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('simultaneous-coop') != -1 && game.multiplayer['simultaneous-coop'] !== true) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('alternating-coop') != -1 && game.multiplayer['alternating-coop'] !== true) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('simultaneous-vs') != -1 && game.multiplayer['simultaneous-vs'] !== true) {
					delete metadata[systemIndex].games[gameIndex];
				} else if (filters.indexOf('alternating-vs') != -1 && game.multiplayer['alternating-vs'] !== true) {
					delete metadata[systemIndex].games[gameIndex];
				}

			});

			metadata[systemIndex].games = system.games.filter(function(){return true;});

		});

		return metadata;

	};

	var renderMetadata = function(metadata) {

		var html = '';

		metadata.forEach(function(system) {

			var system_heading = system.name.replace(/\s+/g, '-').toLowerCase();
			var system_content = system_heading + '-games';

			html += '<h5 id="' + system_heading + '">';
				html += '<a data-toggle="collapse" data-parent="#games" href="#' + system_content + '" aria-controls="' + system_content + '">';
					html += '<img class="system-icon" src="/img/systems/' + system_heading + '.png">';
					html += '<span>' + system.name + ' (' + system.games.length + ')</span>';
				html += '</a>';
			html += '</h5>';

			html += '<ul id="' + system_content + '" class="collapse" role="tabpanel" aria-labelledby="' + system_heading + '">';

			system.games.forEach(function(game) {

				var compatibility = '';
				var multiplayer = '';
				var simultaneous_coop = '';
				var simultaneous_vs = '';
				var alternating_coop = '';
				var alternating_vs = '';

				if (game.compatibility.pi3 === true) {
					compatibility = ' class="pass"';
				} else if (game.compatibility.pi3 === false) {
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

			if (system.games.length === 0) {
				html += '<li>None</li>';
			}

			html += '</ul>';

		});

		return html;

	};

	return {
		filterMetadata: filterMetadata,
		renderMetadata: renderMetadata,
	};

})();