# MongoDB attributes
import yaml

global patterns
with open('items.yaml') as f:    
    patterns = yaml.load(f, Loader=yaml.FullLoader)

# mongodb_uri = 'mongodb+srv://'+patterns.get("user_name")+":"+patterns.get("pass_word")+'@cluster0.2nsop.mongodb.net/?retryWrites=true&w=majority'
# mongodb_user = patterns.get("user_name")
# port = 8000

mongodb_uri = 'localhost'
mongodb_user = 'nest'
port = 27017