from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from store.models import Category, Product

PRODUCTS = [
    ('Wireless Earbuds', 'Electronics', 1499, 'earbuds', 'Compact wireless earbuds for calls, commutes and everyday listening.'),
    ('Bluetooth Speaker', 'Electronics', 1799, 'speaker', 'Portable sound with rich audio for your desk or weekend.'),
    ('Mechanical Keyboard', 'Electronics', 2999, 'keyboard', 'A satisfying tactile keyboard for work, study and play.'),
    ('Wireless Mouse', 'Electronics', 699, 'mouse', 'A smooth, comfortable wireless mouse for your workspace.'),
    ('Power Bank 20000mAh', 'Electronics', 1299, 'power-bank', 'Reliable portable charging for your everyday devices.'),
    ('Adjustable Phone Stand', 'Accessories', 349, 'phone-stand', 'A sturdy adjustable stand for video calls and hands-free viewing.'),
    ('Thermal Water Bottle', 'Home', 699, 'thermal-bottle', 'A reusable insulated bottle to keep your drink close by.'),
    ('Desktop Organizer', 'Home', 499, 'organizer', 'Keep pens, notes and small desk essentials in one tidy place.'),
    ('Ceramic Planter', 'Home', 399, 'planter', 'A clean ceramic planter for a little greenery at home.'),
    ('Soft Cushion Cover', 'Home', 499, 'cushion', 'A soft textured cushion cover for a quick room refresh.'),
    ('Minimal Table Clock', 'Home', 799, 'table-clock', 'A quiet modern clock for your bedside or work desk.'),
    ('Canvas Tote Bag', 'Accessories', 599, 'tote-bag', 'A roomy reusable tote for errands, books and daily essentials.'),
    ('Classic Sunglasses', 'Accessories', 999, 'sunglasses', 'Timeless everyday sunglasses with a comfortable fit.'),
    ('Classic Fold Wallet', 'Accessories', 899, 'wallet', 'A slim everyday wallet with space for your cards and cash.'),
    ('Everyday Baseball Cap', 'Accessories', 499, 'baseball-cap', 'A lightweight adjustable cap for sunny days outdoors.'),
    ('Pocket Journal', 'Stationery', 149, 'journal', 'A compact notebook for reminders, lists and bright ideas.'),
    ('Fountain Pen Gift Set', 'Stationery', 599, 'pen-set', 'A smooth writing pen with a polished presentation case.'),
    ('Sketch Pencil Kit', 'Stationery', 399, 'pencils', 'A small range of drawing pencils for notes and sketches.'),
    ('Pastel Sticky Notes Set', 'Stationery', 129, 'sticky-notes', 'Colorful note pads to keep tasks and reminders in view.'),
    ('Desk Calendar', 'Stationery', 249, 'desk-calendar', 'A simple flip calendar to keep your plans close at hand.'),
]

COLORS = [
    ('#e3edf2','#d3e6ec','#416878'), ('#e8e6f2','#d8d5ee','#514d7a'),
    ('#e8edde','#d9e7c8','#416043'), ('#f1e7db','#ebdcc7','#765a3b'),
    ('#e5ebf4','#d7e1f0','#445b80'), ('#f2e6dc','#ead8c8','#76513d'),
    ('#deedf0','#d1e6e8','#416a70'), ('#e9e5dd','#ddd5c8','#6b5b49'),
    ('#e2eee4','#d4e6d5','#456b4d'), ('#f2e6e5','#ead6d5','#795456'),
    ('#e5e9ef','#d7dce6','#4f5d75'), ('#f1e8db','#e9dcc8','#765d40'),
    ('#e9e6f1','#dcd8ed','#514d77'), ('#e3e8e4','#d4dfd5','#485f4e'),
    ('#f1e9d7','#e8dbbb','#71603b'), ('#ece6dd','#e0d6c8','#665746'),
    ('#e7eaf1','#d8dfeb','#4d5a74'), ('#e8eee0','#dbe8cd','#4c6942'),
    ('#f1e4dc','#ead6c9','#795541'), ('#e5ebeb','#d5e2e1','#4a6865'),
]

SHAPES = [
    '<rect x="235" y="178" width="170" height="142" rx="55" fill="{ink}"/><path d="M278 222c0-28 15-45 37-45s37 17 37 45v14h-17v-14c0-13-7-21-20-21s-20 8-20 21v14h-17z" fill="#fff" opacity=".82"/><circle cx="305" cy="278" r="12" fill="#fff"/><circle cx="355" cy="278" r="12" fill="#fff"/>',
    '<rect x="245" y="118" width="150" height="235" rx="35" fill="{ink}"/><rect x="270" y="145" width="100" height="12" rx="6" fill="#fff" opacity=".8"/><circle cx="320" cy="246" r="47" fill="#fff" opacity=".88"/><circle cx="320" cy="246" r="29" fill="{accent}"/><circle cx="320" cy="325" r="7" fill="#fff"/>',
    '<rect x="116" y="190" width="408" height="142" rx="20" fill="{ink}"/><rect x="136" y="210" width="368" height="98" rx="10" fill="#fff" opacity=".2"/><g fill="#fff" opacity=".9">{keys}</g>',
    '<path d="M320 98c91 0 151 68 143 157-6 65-49 121-113 128-77 9-146-46-152-125-7-93 38-160 122-160z" fill="{ink}"/><path d="M320 112c74 0 122 54 116 132-5 57-39 103-90 110-61 8-119-37-124-102-6-78 30-140 98-140z" fill="#fff" opacity=".16"/><circle cx="320" cy="310" r="8" fill="#fff"/>',
    '<rect x="190" y="115" width="260" height="245" rx="34" fill="{ink}"/><rect x="215" y="145" width="210" height="180" rx="19" fill="#fff" opacity=".18"/><rect x="262" y="203" width="110" height="38" rx="15" fill="#fff" opacity=".88"/><circle cx="393" cy="222" r="8" fill="#fff"/>',
    '<path d="M270 326h100l-16-126h-68z" fill="{ink}"/><path d="M268 204l45-59 44 59" fill="none" stroke="{ink}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><rect x="295" y="297" width="50" height="13" rx="6" fill="#fff" opacity=".9"/>',
    '<rect x="246" y="123" width="148" height="230" rx="38" fill="{ink}"/><rect x="263" y="108" width="114" height="31" rx="10" fill="{accent}"/><rect x="263" y="157" width="114" height="168" rx="25" fill="#fff" opacity=".16"/><path d="M290 190h60" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".75"/>',
    '<rect x="153" y="182" width="334" height="168" rx="20" fill="{ink}"/><rect x="176" y="205" width="288" height="53" rx="12" fill="#fff" opacity=".2"/><path d="M210 281h220M210 311h160" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/>',
    '<path d="M224 226h192l-24 129H248z" fill="{ink}"/><ellipse cx="320" cy="226" rx="96" ry="28" fill="{accent}"/><path d="M319 229c-8-64 23-108 61-129M317 226c-46-50-81-53-106-37M319 225c5-42-3-78-27-111" fill="none" stroke="#5d9663" stroke-width="13" stroke-linecap="round"/><ellipse cx="382" cy="110" rx="21" ry="38" transform="rotate(39 382 110)" fill="#78a878"/><ellipse cx="207" cy="187" rx="20" ry="36" transform="rotate(-60 207 187)" fill="#78a878"/>',
    '<rect x="176" y="150" width="288" height="205" rx="35" fill="{ink}"/><rect x="198" y="172" width="244" height="161" rx="26" fill="#fff" opacity=".12"/><path d="M205 180l230 145M435 180L205 325" stroke="#fff" stroke-width="5" opacity=".35"/>',
    '<circle cx="320" cy="242" r="119" fill="{ink}"/><circle cx="320" cy="242" r="99" fill="#fff" opacity=".92"/><circle cx="320" cy="242" r="86" fill="{accent}"/><circle cx="320" cy="242" r="72" fill="#fff"/><path d="M320 190v55l42 29" fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round"/><circle cx="320" cy="242" r="8" fill="{ink}"/>',
    '<path d="M186 197h268l-27 158H213z" fill="{ink}"/><path d="M244 203v-42c0-88 152-88 152 0v42" fill="none" stroke="{ink}" stroke-width="16"/><path d="M215 235h210" stroke="#fff" stroke-width="7" opacity=".75"/>',
    '<path d="M164 205h133c10-51 96-51 106 0h73v104H164z" fill="{ink}"/><path d="M179 223h332" stroke="#fff" stroke-width="7" opacity=".65"/><path d="M180 250h91M352 250h138" stroke="#fff" stroke-width="5" opacity=".45"/>',
    '<rect x="181" y="154" width="278" height="193" rx="26" fill="{ink}"/><path d="M181 208h278" stroke="#fff" stroke-width="7" opacity=".35"/><path d="M207 240h220v83H207z" fill="#fff" opacity=".16"/><path d="M320 154v193" stroke="#fff" stroke-width="5" opacity=".5"/>',
    '<path d="M180 226c5-73 68-119 140-119s135 46 140 119H180z" fill="{ink}"/><path d="M180 226h280c-10 29-43 47-101 49l-179-10z" fill="{accent}"/><path d="M232 207c19-28 48-41 88-41" stroke="#fff" stroke-width="7" fill="none" opacity=".6"/>',
    '<rect x="187" y="111" width="266" height="260" rx="10" fill="{ink}"/><rect x="213" y="134" width="218" height="211" rx="5" fill="#fff" opacity=".9"/><path d="M237 180h172M237 207h172M237 234h145M237 261h172M237 288h139" stroke="{ink}" stroke-width="5" opacity=".35"/><path d="M207 131v220" stroke="{accent}" stroke-width="13"/>',
    '<rect x="210" y="113" width="220" height="235" rx="26" fill="{ink}"/><rect x="228" y="135" width="184" height="185" rx="13" fill="#fff" opacity=".18"/><path d="M280 122l-22 178M320 122l-22 178M360 122l-22 178" stroke="#fff" stroke-width="12" stroke-linecap="round"/><path d="M265 303l-8 34 27-23M305 303l-8 34 27-23M345 303l-8 34 27-23" fill="{accent}"/>',
    '<rect x="204" y="166" width="238" height="188" rx="14" fill="{ink}" opacity=".35"/><rect x="184" y="144" width="238" height="188" rx="14" fill="{accent}"/><rect x="164" y="122" width="238" height="188" rx="14" fill="{ink}"/><path d="M194 174h177M194 205h144M194 236h160" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/><path d="M344 122h58v58" fill="#fff" opacity=".35"/>',
    '<rect x="204" y="166" width="238" height="188" rx="14" fill="{ink}" opacity=".35"/><rect x="184" y="144" width="238" height="188" rx="14" fill="{accent}"/><rect x="164" y="122" width="238" height="188" rx="14" fill="{ink}"/><path d="M194 174h177M194 205h144M194 236h160" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/><path d="M344 122h58v58" fill="#fff" opacity=".35"/>',
    '<rect x="201" y="112" width="238" height="242" rx="18" fill="{ink}"/><rect x="220" y="132" width="200" height="49" rx="9" fill="#fff" opacity=".88"/><path d="M240 132v-17a9 9 0 0118 0v17m53 0v-17a9 9 0 0118 0v17m53 0v-17a9 9 0 0118 0v17" stroke="{accent}" stroke-width="7" fill="none"/><g fill="#fff" opacity=".82"><circle cx="256" cy="219" r="8"/><circle cx="320" cy="219" r="8"/><circle cx="384" cy="219" r="8"/><circle cx="256" cy="268" r="8"/><circle cx="320" cy="268" r="8"/><circle cx="384" cy="268" r="8"/><circle cx="256" cy="317" r="8"/><circle cx="320" cy="317" r="8"/><circle cx="384" cy="317" r="8"/></g>',
]

class Command(BaseCommand):
    help = 'Create the V.M.S demo collection: 20 products with individual SVG artwork.'

    def handle(self, *args, **options):
        media = Path(settings.MEDIA_ROOT) / 'products'
        media.mkdir(parents=True, exist_ok=True)
        keys = ''.join(f'<rect x="{145 + col*41}" y="{219 + row*27}" width="29" height="16" rx="4"/>' for row in range(3) for col in range(8))
        added = 0
        for idx, (name, category_name, price, slug, description) in enumerate(PRODUCTS):
            bg, accent, ink = COLORS[idx]
            shape = SHAPES[idx]
            if slug == 'keyboard': shape = shape.replace('{keys}', keys)
            drawing = shape.format(ink=ink, accent=accent)
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480" role="img" aria-label="{name}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{accent}"/></linearGradient><filter id="shadow" x="-.3" y="-.3" width="1.6" height="1.8"><feGaussianBlur in="SourceAlpha" stdDeviation="10"/><feOffset dy="12"/><feComponentTransfer><feFuncA type="linear" slope=".16"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="640" height="480" rx="38" fill="url(#bg)"/><circle cx="522" cy="95" r="92" fill="#fff" opacity=".22"/><circle cx="106" cy="379" r="76" fill="#fff" opacity=".18"/><ellipse cx="320" cy="379" rx="181" ry="23" fill="{ink}" opacity=".12"/><g filter="url(#shadow)">{drawing}</g><path d="M90 420h460" stroke="#fff" stroke-width="2" opacity=".35"/></svg>'''
            image_name = f'products/{slug}.svg'
            (media / f'{slug}.svg').write_text(svg, encoding='utf-8')
            category, _ = Category.objects.get_or_create(name=category_name)
            product, created = Product.objects.get_or_create(name=name, defaults={
                'category': category, 'price': price, 'stock': 25,
                'image': image_name, 'description': description,
            })
            if created:
                added += 1
            elif not product.image:
                product.image = image_name
                product.save(update_fields=['image'])
        self.stdout.write(self.style.SUCCESS(f'Product catalog ready. {added} new products added; {len(PRODUCTS)} catalog products ensured.'))
