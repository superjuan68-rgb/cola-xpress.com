import json, re, os

base = r'C:\Users\j-pre\OneDrive\Documents\public_html'
checks = [
    'grow/dwc-basics-for-beginners.html',
    'learn/harvest-ripeness.html',
    'equipment/what-to-buy-first.html',
    'grow/root-problems-in-dwc.html',
]
for rel in checks:
    path = os.path.join(base, rel.replace('/', os.sep))
    with open(path, encoding='utf-8') as f:
        html = f.read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    imageobj_blocks = [b for b in blocks if 'ImageObject' in b]
    print(f'{rel}: {len(imageobj_blocks)} ImageObject block(s)')
    for b in imageobj_blocks:
        try:
            data = json.loads(b.strip())
            if '@graph' in data:
                for obj in data['@graph']:
                    fname = obj['contentUrl'].split('/')[-1]
                    desc  = obj.get('description', '')
                    print(f'  {fname}  |  {len(desc)} char alt  |  {obj["width"]}x{obj["height"]}')
            else:
                fname = data['contentUrl'].split('/')[-1]
                desc  = data.get('description', '')
                print(f'  {fname}  |  {len(desc)} char alt  |  {data["width"]}x{data["height"]}')
            print(f'  JSON: VALID')
        except json.JSONDecodeError as e:
            print(f'  JSON: INVALID -- {e}')
    print()
