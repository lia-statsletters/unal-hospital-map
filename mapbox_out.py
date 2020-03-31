from jinja2 import Template
import os, json, re

def map_maker(layers, mapbox_key, city_config, city_text='city', maphtml=''):
    with open(maphtml, 'r') as f:
        template = Template(f.read())
    #ugly but simple, ToDo fix later
    ljsons={}
    for layer in [json.loads(x) for x in layers]:
        try:
            ljsons[layer['category']].append(layer['id'])
        except:
            ljsons[layer['category']]=[layer['id']]
    ljsons={k:sorted(ljsons[k]) for k in ljsons }

    out = template.render(layers=layers, mapbox_key=mapbox_key,
                          catlist=ljsons.keys(), menudict=ljsons,
                          **city_config)#mapbox_style=mapbox_style)
    with open(f"./.to_ignore/{city_text}_mapbox.html", "w") as fh:
        fh.write(out)
    return out


if __name__ == "__main__":
    city='bogota'
    city_templates=f'./templates/{city}'
    #Load City Config
    city_config=f'{city_templates}/city_config.json'
    with open(city_config, 'r') as f:
        city_config = json.loads(f.read())
        
    #Load City Layers
    data_path = f'./data/{city}'
    layers_path = f'{city_templates}/layers'
    layers=[]
    for filex in os.listdir(os.fsencode(layers_path)):
        fn = os.fsdecode(filex)
        toread_layer = f'{layers_path}/{fn}'
        
        try:
            with open(toread_layer, 'r') as f: #get json
                layer=f.read()
                layer=Template(layer)
            fk=layer.render(dt=' "xx" ')
            fk=re.sub("'", '"', fk)
            fk=json.loads(fk)
            fk=fk["srcfile"]
            toread_data = f'{data_path}/{fk}'
            with open(toread_data, 'r') as f: #add data to json
                layer_data=f.read()
            layer=layer.render(dt=layer_data)
            layer = re.sub("'", '"', layer)
            layers.append(layer)
        except Exception as HELL:
            continue

    # Load Mapbox Key
    mapbox_key = './.to_ignore/keys/mapbox.key'
    with open(mapbox_key, mode='r') as thefile:
        for line in thefile:
            mapbox_key = line[:-1]
            break
    out_html = map_maker(layers, mapbox_key, city_config,city_text=city,
                         maphtml='./templates/fancy_geojson_mapbox.html',
                         )