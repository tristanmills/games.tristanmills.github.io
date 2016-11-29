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

	var renderGames = function(games) {

		var html = '';

		html += '<ul>';

		games.forEach(function(game) {

			var compatibility = '';
			var multiplayer = '';
			var simultaneousCoOp = '';
			var simultaneousVS = '';
			var alternatingCoOp = '';
			var alternatingVS = '';

			if (game.compatibility.pi3 === true) {
				compatibility = ' class="pass"';
			} else if (game.compatibility.pi3 === false) {
				compatibility = ' class="fail"';
			}

			if (game.players > 1) {
				multiplayer = ' <span class="tag tag-info">Multi (' + game.players + ')</span>';
			}

			if (game.multiplayer['simultaneous-coop']) {
				simultaneousCoOp = ' <span class="tag tag-success">Simo Co-Op</span>';
			}

			if (game.multiplayer['alternating-coop']) {
				alternatingCoOp = ' <span class="tag tag-success">Alt Co-Op</span>';
			}

			if (game.multiplayer['simultaneous-vs']) {
				simultaneousVS = ' <span class="tag tag-danger">Simo Vs</span>';
			}

			if (game.multiplayer['alternating-vs']) {
				alternatingVS = ' <span class="tag tag-danger">Alt Vs</span>';
			}

			html += '<li' + compatibility + '>' + game.name + multiplayer + simultaneousCoOp + alternatingCoOp + simultaneousVS + alternatingVS + '</li>';

		});

		if (games.length === 0) {
			html += '<li>None</li>';
		}

		html += '</ul>';

		return html;
	};

	var renderMetadata = function(metadata) {

		var html = '';

		metadata.forEach(function(system) {

			var licensedGames = [];
			var unlicensedGames = [];

			system.games.forEach(function(game) {

				if (game.licensed) {

					licensedGames.push(game);

				} else {

					unlicensedGames.push(game);

				}

			});

			var systemHeading = system.name.replace(/\s+/g, '-').toLowerCase();
			var systemContent = systemHeading + '-games';

			var complete = '';

			if (system.licensed !== null) {
				complete = ' (Complete)';
			}

			html += '<h5 id="' + systemHeading + '">';
				html += '<a data-toggle="collapse" data-parent="#games" href="#' + systemContent + '" aria-controls="' + systemContent + '">';
					html += '<img class="system-icon" src="/img/systems/' + systemHeading + '.png">';
					html += '<span>' + system.name + complete + ' (' + system.games.length + ')</span>';
				html += '</a>';
			html += '</h5>';

			html += '<div id="' + systemContent + '" class="collapse" role="tabpanel" aria-labelledby="' + systemHeading + '">';

			html += '<h6>Licensed</h6>';

			html += renderGames(licensedGames);

			html += '<h6>Unlicensed</h6>';

			html += renderGames(unlicensedGames);

			html += '</div>';

		});

		return html;

	};

	return {
		filterMetadata: filterMetadata,
		renderMetadata: renderMetadata,
	};

})();