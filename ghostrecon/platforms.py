"""Platform definitions.

Every entry here was checked against the live internet with
`python3 tools/verify_platforms.py`; VERIFICATION.md records the raw evidence.
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
]
