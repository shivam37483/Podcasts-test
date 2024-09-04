import yaml
import xml.etree.ElementTree as xml_tree

# Define namespaces
NSMAP = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'content': 'http://purl.org/rss/1.0/modules/content/'
}

# Register namespaces
for prefix, uri in NSMAP.items():
    xml_tree.register_namespace(prefix, uri)

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    # Create RSS element with namespaces
    rss_element = xml_tree.Element('rss', {
        'version': '2.0'
    })
    
    # Create channel element
    channel_element = xml_tree.SubElement(rss_element, 'channel')

    link_prefix = yaml_data['link']

    # Populate the channel element with data from YAML
    xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}image', {'href': link_prefix + yaml_data['image']})

    xml_tree.SubElement(channel_element, 'link').text = link_prefix
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}category', {'text': yaml_data['category']})

    # Create item elements for each item in the YAML
    for item in yaml_data['item']:
        item_element = xml_tree.SubElement(channel_element, 'item')
 
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text = item['duration']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']

        # Handle enclosure element with proper type casting for length
        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + item['file'],
            'type': 'audio/mpeg',
            'length': str(item['length'])  # Ensure this is a string
        })

    # Output the RSS feed as an XML file
    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', xml_declaration=True, encoding='UTF-8')
