format_chars = {
	'Ã©':	'é',
	' Ã ':	'à',
	'Ã':	'û',
	'Ã§':	'ç',
	'Ãª':	'ê',
	'Ã¨':	'è',
	'Ã´':	'ô',
	'Â':	'',
	'€™':	'’',
}


format_invalid = {
	r'(\n+)':	'\n',
	r'(\t+)':	'\t',
	'\xa0':		' '
}

format_balises_names = {
	'p':		'',
	'em':		'',
	'span':		'',
	'br':		'**'
}

balises_pattern = '<{0}>([^<]*)</{0}>'