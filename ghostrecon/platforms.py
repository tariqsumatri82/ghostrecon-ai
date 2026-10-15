"""Platform definitions.

Every entry here was checked against the live internet with
`python3 tools/verify_platforms.py`; tools/verification_report.txt records the raw evidence.
Adding a platform is a one-line change to this list and nothing else.

Fields:
    name, category, url   required; url contains the {username} placeholder
    check                 "status" (default) or "marker"
    found_codes           HTTP codes meaning "profile exists"   (default (200,))
    missing_codes         HTTP codes meaning "no profile"       (default (404,))
    missing_markers       page text meaning "no profile" even on HTTP 200
    found_markers         page text that must appear for 200 to mean "found"
    note                  caveat shown in --verbose and JSON output
"""

PLATFORMS = [
    {
        'name': 'GitHub',
        'category': 'developer',
        'url': 'https://github.com/{username}',
    },
    {
        'name': 'Codeberg',
        'category': 'developer',
        'url': 'https://codeberg.org/{username}',
    },
    {
        'name': 'Gitea.com',
        'category': 'developer',
        'url': 'https://gitea.com/{username}',
    },
    {
        'name': 'Bitbucket',
        'category': 'developer',
        'url': 'https://bitbucket.org/{username}/',
    },
    {
        'name': 'Launchpad',
        'category': 'developer',
        'url': 'https://launchpad.net/~{username}',
    },
    {
        'name': 'Docker Hub',
        'category': 'developer',
        'url': 'https://hub.docker.com/u/{username}',
    },
    {
        'name': 'Hugging Face',
        'category': 'developer',
        'url': 'https://huggingface.co/{username}',
    },
    {
        'name': 'Kaggle',
        'category': 'developer',
        'url': 'https://www.kaggle.com/{username}',
    },
    {
        'name': 'Replit',
        'category': 'developer',
        'url': 'https://replit.com/@{username}',
    },
    {
        'name': 'Netlify',
        'category': 'developer',
        'url': 'https://{username}.netlify.app',
    },
    {
        'name': 'DigitalOcean',
        'category': 'developer',
        'url': 'https://www.digitalocean.com/community/users/{username}',
    },
    {
        'name': 'OpenCollective',
        'category': 'developer',
        'url': 'https://opencollective.com/{username}',
    },
    {
        'name': 'Liberapay',
        'category': 'developer',
        'url': 'https://liberapay.com/{username}/',
    },
    {
        'name': 'Dev.to',
        'category': 'developer',
        'url': 'https://dev.to/{username}',
    },
    {
        'name': 'Zenn',
        'category': 'developer',
        'url': 'https://zenn.dev/{username}',
    },
    {
        'name': 'Qiita',
        'category': 'developer',
        'url': 'https://qiita.com/{username}',
    },
    {
        'name': 'Lobsters',
        'category': 'developer',
        'url': 'https://lobste.rs/~{username}',
    },
    {
        'name': 'Hacker News',
        'category': 'developer',
        'url': 'https://news.ycombinator.com/user?id={username}',
        'check': 'marker',
        'missing_markers': ['no such user'],
    },
    {
        'name': 'Keybase',
        'category': 'security',
        'url': 'https://keybase.io/{username}',
    },
    {
        'name': 'Bugcrowd',
        'category': 'security',
        'url': 'https://bugcrowd.com/{username}',
    },
    {
        'name': 'HackerOne',
        'category': 'security',
        'url': 'https://hackerone.com/{username}',
    },
    {
        'name': 'Mastodon.social',
        'category': 'social',
        'url': 'https://mastodon.social/@{username}',
    },
    {
        'name': 'Bluesky',
        'category': 'social',
        'url': 'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={username}.bsky.social',
        'missing_codes': [400, 404],
    },
    {
        'name': 'VK',
        'category': 'social',
        'url': 'https://vk.com/{username}',
    },
    {
        'name': 'Disqus',
        'category': 'social',
        'url': 'https://disqus.com/by/{username}/',
    },
    {
        'name': 'Linktree',
        'category': 'social',
        'url': 'https://linktr.ee/{username}',
    },
    {
        'name': 'Gravatar',
        'category': 'social',
        'url': 'https://gravatar.com/{username}',
    },
    {
        'name': 'YouTube',
        'category': 'media',
        'url': 'https://www.youtube.com/@{username}',
    },
    {
        'name': 'Vimeo',
        'category': 'media',
        'url': 'https://vimeo.com/{username}',
    },
    {
        'name': 'SoundCloud',
        'category': 'media',
        'url': 'https://soundcloud.com/{username}',
    },
    {
        'name': 'Spotify',
        'category': 'media',
        'url': 'https://open.spotify.com/user/{username}',
    },
    {
        'name': 'Bandcamp',
        'category': 'media',
        'url': 'https://bandcamp.com/{username}',
    },
    {
        'name': 'Mixcloud',
        'category': 'media',
        'url': 'https://www.mixcloud.com/{username}/',
    },
    {
        'name': 'Flickr',
        'category': 'media',
        'url': 'https://www.flickr.com/people/{username}',
    },
    {
        'name': 'Behance',
        'category': 'design',
        'url': 'https://www.behance.net/{username}',
    },
    {
        'name': 'Dribbble',
        'category': 'design',
        'url': 'https://dribbble.com/{username}',
    },
    {
        'name': 'DeviantArt',
        'category': 'design',
        'url': 'https://www.deviantart.com/{username}',
    },
    {
        'name': 'Substack',
        'category': 'writing',
        'url': 'https://{username}.substack.com',
    },
    {
        'name': 'Wattpad',
        'category': 'writing',
        'url': 'https://www.wattpad.com/user/{username}',
    },
    {
        'name': 'Goodreads',
        'category': 'writing',
        'url': 'https://www.goodreads.com/{username}',
    },
    {
        'name': 'Speaker Deck',
        'category': 'writing',
        'url': 'https://speakerdeck.com/{username}',
    },
    {
        'name': 'Steam',
        'category': 'gaming',
        'url': 'https://steamcommunity.com/id/{username}',
        'check': 'marker',
        'missing_markers': ['The specified profile could not be found', 'no such user'],
    },
    {
        'name': 'Chess.com',
        'category': 'gaming',
        'url': 'https://www.chess.com/member/{username}',
    },
    {
        'name': 'MyAnimeList',
        'category': 'gaming',
        'url': 'https://myanimelist.net/profile/{username}',
    },
    {
        'name': 'Patreon',
        'category': 'commerce',
        'url': 'https://www.patreon.com/{username}',
    },
    {
        'name': 'Buy Me a Coffee',
        'category': 'commerce',
        'url': 'https://buymeacoffee.com/{username}',
    },
    {
        'name': 'Gumroad',
        'category': 'commerce',
        'url': 'https://gumroad.com/{username}',
    },
    {
        'name': 'OpenStreetMap',
        'category': 'misc',
        'url': 'https://www.openstreetmap.org/user/{username}',
    },
    {
        'name': 'Wikipedia',
        'category': 'misc',
        'url': 'https://en.wikipedia.org/wiki/User:{username}',
    },
    {
        'name': 'Are.na',
        'category': 'misc',
        'url': 'https://www.are.na/{username}',
    },
    {
        'name': 'Slashdot',
        'category': 'misc',
        'url': 'https://slashdot.org/~{username}',
    },
    {
        'name': 'Indie Hackers',
        'category': 'misc',
        'url': 'https://www.indiehackers.com/{username}',
    },
    {
        'name': 'Gitee',
        'category': 'developer',
        'url': 'https://gitee.com/{username}',
    },
    {
        'name': 'SourceForge',
        'category': 'developer',
        'url': 'https://sourceforge.net/u/{username}/profile',
    },
    {
        'name': 'StackBlitz',
        'category': 'developer',
        'url': 'https://stackblitz.com/@{username}',
    },
    {
        'name': 'Codewars',
        'category': 'developer',
        'url': 'https://www.codewars.com/users/{username}',
    },
    {
        'name': 'HackerEarth',
        'category': 'developer',
        'url': 'https://www.hackerearth.com/@{username}',
    },
    {
        'name': 'AtCoder',
        'category': 'developer',
        'url': 'https://atcoder.jp/users/{username}',
    },
    {
        'name': 'RubyGems',
        'category': 'developer',
        'url': 'https://rubygems.org/profiles/{username}',
    },
    {
        'name': 'DZone',
        'category': 'developer',
        'url': 'https://dzone.com/users/{username}',
    },
    {
        'name': 'Hacker Noon',
        'category': 'developer',
        'url': 'https://hackernoon.com/u/{username}',
    },
    {
        'name': 'Codementor',
        'category': 'developer',
        'url': 'https://www.codementor.io/@{username}',
    },
    {
        'name': 'Hackaday',
        'category': 'developer',
        'url': 'https://hackaday.io/{username}',
    },
    {
        'name': 'Hackster',
        'category': 'developer',
        'url': 'https://www.hackster.io/{username}',
    },
    {
        'name': 'Instructables',
        'category': 'developer',
        'url': 'https://www.instructables.com/member/{username}/',
    },
    {
        'name': 'Devfolio',
        'category': 'developer',
        'url': 'https://devfolio.co/@{username}',
    },
    {
        'name': 'WordPress.org',
        'category': 'developer',
        'url': 'https://profiles.wordpress.org/{username}/',
    },
    {
        'name': 'Drupal.org',
        'category': 'developer',
        'url': 'https://www.drupal.org/u/{username}',
    },
    {
        'name': 'Coderwall',
        'category': 'developer',
        'url': 'https://coderwall.com/{username}',
    },
    {
        'name': 'X',
        'category': 'social',
        'url': 'https://x.com/{username}',
    },
    {
        'name': 'Snapchat',
        'category': 'social',
        'url': 'https://www.snapchat.com/add/{username}',
    },
    {
        'name': 'Infosec Exchange',
        'category': 'social',
        'url': 'https://infosec.exchange/@{username}',
    },
    {
        'name': 'mstdn.social',
        'category': 'social',
        'url': 'https://mstdn.social/@{username}',
    },
    {
        'name': 'Mastodon.online',
        'category': 'social',
        'url': 'https://mastodon.online/@{username}',
    },
    {
        'name': 'mas.to',
        'category': 'social',
        'url': 'https://mas.to/@{username}',
    },
    {
        'name': 'techhub.social',
        'category': 'social',
        'url': 'https://techhub.social/@{username}',
    },
    {
        'name': 'Gab',
        'category': 'social',
        'url': 'https://gab.com/{username}',
    },
    {
        'name': 'Minds',
        'category': 'social',
        'url': 'https://www.minds.com/{username}',
    },
    {
        'name': '9GAG',
        'category': 'social',
        'url': 'https://9gag.com/u/{username}',
    },
    {
        'name': 'Douban',
        'category': 'social',
        'url': 'https://www.douban.com/people/{username}/',
    },
    {
        'name': 'Naver Blog',
        'category': 'social',
        'url': 'https://blog.naver.com/{username}',
    },
    {
        'name': 'Pixelfed.social',
        'category': 'social',
        'url': 'https://pixelfed.social/{username}',
    },
    {
        'name': 'TMDB',
        'category': 'media',
        'url': 'https://www.themoviedb.org/u/{username}',
    },
    {
        'name': 'SmugMug',
        'category': 'media',
        'url': 'https://{username}.smugmug.com',
    },
    {
        'name': 'Tapas',
        'category': 'media',
        'url': 'https://tapas.io/{username}',
    },
    {
        'name': 'Sketchfab',
        'category': 'design',
        'url': 'https://sketchfab.com/{username}',
    },
    {
        'name': 'Cara',
        'category': 'design',
        'url': 'https://cara.app/{username}',
    },
    {
        'name': 'Steemit',
        'category': 'writing',
        'url': 'https://steemit.com/@{username}',
    },
    {
        'name': 'Issuu',
        'category': 'writing',
        'url': 'https://issuu.com/{username}',
    },
    {
        'name': 'LiveJournal',
        'category': 'writing',
        'url': 'https://{username}.livejournal.com',
    },
    {
        'name': 'Write.as',
        'category': 'writing',
        'url': 'https://write.as/{username}',
    },
    {
        'name': 'Bear Blog',
        'category': 'writing',
        'url': 'https://{username}.bearblog.dev',
    },
    {
        'name': 'Neocities',
        'category': 'writing',
        'url': 'https://{username}.neocities.org',
    },
    {
        'name': 'osu!',
        'category': 'gaming',
        'url': 'https://osu.ppy.sh/users/{username}',
    },
    {
        'name': 'itch.io',
        'category': 'gaming',
        'url': 'https://{username}.itch.io',
    },
    {
        'name': 'GOG',
        'category': 'gaming',
        'url': 'https://www.gog.com/u/{username}',
    },
    {
        'name': 'Wise Old Man',
        'category': 'gaming',
        'url': 'https://wiseoldman.net/players/{username}',
    },
    {
        'name': 'Venmo',
        'category': 'commerce',
        'url': 'https://venmo.com/u/{username}',
    },
    {
        'name': 'Cash App',
        'category': 'commerce',
        'url': 'https://cash.app/${username}',
    },
    {
        'name': 'OpenSea',
        'category': 'commerce',
        'url': 'https://opensea.io/{username}',
    },
    {
        'name': 'Zora',
        'category': 'commerce',
        'url': 'https://zora.co/{username}',
    },
    {
        'name': 'Threadless',
        'category': 'commerce',
        'url': 'https://www.threadless.com/@{username}',
    },
    {
        'name': 'Spreadshirt',
        'category': 'commerce',
        'url': 'https://www.spreadshirt.com/shop/{username}/',
    },
    {
        'name': 'Poshmark',
        'category': 'commerce',
        'url': 'https://poshmark.com/closet/{username}',
    },
    {
        'name': 'Grailed',
        'category': 'commerce',
        'url': 'https://www.grailed.com/{username}',
    },
    {
        'name': 'Big Cartel',
        'category': 'commerce',
        'url': 'https://{username}.bigcartel.com',
    },
    {
        'name': 'Whatnot',
        'category': 'commerce',
        'url': 'https://www.whatnot.com/user/{username}',
    },
    {
        'name': 'Freelancer',
        'category': 'commerce',
        'url': 'https://www.freelancer.com/u/{username}',
    },
    {
        'name': 'Wellfound',
        'category': 'commerce',
        'url': 'https://wellfound.com/u/{username}',
    },
    {
        'name': 'StockTwits',
        'category': 'commerce',
        'url': 'https://stocktwits.com/{username}',
    },
    {
        'name': 'TradingView',
        'category': 'commerce',
        'url': 'https://www.tradingview.com/u/{username}/',
    },
    {
        'name': 'Wikidata',
        'category': 'misc',
        'url': 'https://www.wikidata.org/wiki/User:{username}',
    },
    {
        'name': 'Wikimedia Commons',
        'category': 'misc',
        'url': 'https://commons.wikimedia.org/wiki/User:{username}',
    },
    {
        'name': 'Komoot',
        'category': 'misc',
        'url': 'https://www.komoot.com/user/{username}',
    },
    {
        'name': 'Untappd',
        'category': 'misc',
        'url': 'https://untappd.com/user/{username}',
    },
    {
        'name': 'Memrise',
        'category': 'misc',
        'url': 'https://www.memrise.com/user/{username}/',
    },
    {
        'name': 'Calendly',
        'category': 'misc',
        'url': 'https://calendly.com/{username}',
    },
    {
        'name': 'Cal.com',
        'category': 'misc',
        'url': 'https://cal.com/{username}',
    },
    {
        'name': 'Carrd',
        'category': 'misc',
        'url': 'https://{username}.carrd.co',
    },
    {
        'name': 'solo.to',
        'category': 'misc',
        'url': 'https://solo.to/{username}',
    },
    {
        'name': 'AllMyLinks',
        'category': 'misc',
        'url': 'https://allmylinks.com/{username}',
    },
    {
        'name': 'Zotero',
        'category': 'misc',
        'url': 'https://www.zotero.org/{username}',
    },
]
