from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    'shield': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 '
        '11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 '
        '9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/>'
        '</svg>'
    ),
    'chart': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"/>'
        '</svg>'
    ),
    'clock': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/>'
        '</svg>'
    ),
    'key': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 '
        '17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 '
        '.43-1.563A6 6 0 1121.75 8.25z"/>'
        '</svg>'
    ),
    'eye': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 '
        '8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 '
        '0-8.573-3.007-9.963-7.178z"/>'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>'
        '</svg>'
    ),
    'checkmark': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
        '</svg>'
    ),
    'star': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04 '
        '.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 '
        '0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 '
        '0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"/>'
        '</svg>'
    ),
    'map': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>'
        '</svg>'
    ),
    'phone': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/>'
        '</svg>'
    ),
    'email': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/>'
        '</svg>'
    ),
    'location': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>'
        '</svg>'
    ),
    'external': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"/>'
        '</svg>'
    ),
    'arrow-right': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/>'
        '</svg>'
    ),
    'seller': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"/>'
        '</svg>'
    ),
    'buyer': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/>'
        '</svg>'
    ),
    'prozorro': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418"/>'
        '</svg>'
    ),
    'check': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>'
        '</svg>'
    ),
    'warning': (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
        'viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>'
        '</svg>'
    ),
}


@register.simple_tag
def icon(name, **kwargs):
    svg = ICONS.get(name, ICONS['checkmark'])
    return mark_safe(svg)


@register.filter
def nl2li(value):
    """Convert newline-separated text to HTML list items."""
    lines = [l.strip() for l in value.split('\n') if l.strip()]
    items = ''.join(f'<li>{line}</li>' for line in lines)
    return mark_safe(f'<ul>{items}</ul>')
