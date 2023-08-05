import boto3
import logging

class ImageIdsTableHelper:
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.table_name = 'ColorSplashImageIds'
        self.image_id_attribute_key = 'ImageId'
        self.full_url_attribute_key = 'FullURL'
        self.regular_url_attribute_key = 'RegularURL'
        self.small_url_attribute_key = 'SmallURL'
        self.thumbnail_url_attribute_key = 'ThumbnailURL'

    def get_key(self, key):
        '''Given a ImageId key, retrieve the remaing attributes and deserialize it into native 
        python types'''

        if key is None:
            raise TypeError("Parameter 'key' cannot be of type None")

        try:
            response = self.client.get_item(
                Key={
                    self.image_id_attribute_key: {
                        'S': key
                    }
                },
                TableName=self.table_name
            )

            if 'Item' not in response:
                raise KeyError("No such key: " + key)
            else:
                return self.deserialize_urls(response['Item'])
        
        except Exception as e:
            logging.error(e)
            raise

    def deserialize_urls(self, serialized_items):
        ''' Given a row of the table, deserialize the DynamoDB specific format into python native types'''
        logging.debug(serialized_items)

        urls = {}
        for key, value in serialized_items.items():
            urls[key] = self.deserialize_string(value)

        return urls

    def deserialize_string(self, string_attribute):
        ''' Given a string dynamodb row attribute, deserialize it'''
        if 'S' not in string_attribute:
            raise ValueError("Missing String('S') data in attribute")  

        return string_attribute['S']