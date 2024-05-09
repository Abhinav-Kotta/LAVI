from transformers import DistilBertTokenizer, DistilBertModel
import torch
import re
import json
import random
import torch.nn as nn

device = torch.device('cpu')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

label_decoder = {
    0: 'FAQ',#faq
    1: 'feedback',#thoughts
    2: 'menu',#menu
    3: 'career growth',#growth opportunities
    4: 'communication methods',#communication
    5: 'company',#company
    6: 'diversity inclusion',#diversity and inclusion
    7: 'goodbye',#farewell
    8: 'greeting',#hello
    9: 'help',#help
    10: 'introduction',#who are you
    11: 'job details',#role
    12: 'leadership style',#leader
    13: 'noanswer',
    14: 'salary',#salary
    15: 'work environment'#work culture
}

def get_file():
    filename = 'intents.json'  # Replace 'file.txt' with your file's name
    
    # Use send_file to send the file to the client
    return send_file(filename, as_attachment=True)
    # 'as_attachment=True' prompts the browser to download the file

class BERT_Arch(nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert = bert

        # dropout layer
        self.dropout = nn.Dropout(0.2)

        # relu activation function
        self.relu =  nn.ReLU()
        # dense layer
        self.fc1 = nn.Linear(768,512)
        self.fc2 = nn.Linear(512,256)
        self.fc3 = nn.Linear(256,128)
        self.fc4 = nn.Linear(128,64)
        self.fc5 = nn.Linear(64,32)
        self.fc6 = nn.Linear(32,16)
        #softmax activation function
        self.softmax = nn.Softmax(dim=1)
        #define the forward pass
    def forward(self, sent_id, mask):
        #pass the inputs to the model
        cls_hs = self.bert(sent_id, attention_mask=mask)[0][:,0]

        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc3(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc4(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc5(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc6(x)

        # apply softmax activation
        x = self.softmax(x)
        return x

# Recreate the model architecture
loaded_model = BERT_Arch(bert)

loaded_model = loaded_model.to(device)

# Load the saved weights
loaded_model.load_state_dict(torch.load('./bert_model.pth', map_location=torch.device('cpu')))

# Set the model to evaluation mode
loaded_model.eval()

def classify_intent(sample_sentence):
    sample_sentence = re.sub(r'[^a-zA-Z ]+', "", sample_sentence)

    # Run a test sample (assuming you have a sample sentence and its corresponding mask)
    encoded_input = tokenizer(
        sample_sentence,
        max_length=16,
        padding="max_length",
        return_token_type_ids=False,
        return_tensors='pt'
    )
    input_ids = encoded_input['input_ids'].to(device)
    attention_mask = encoded_input['attention_mask'].to(device)

    # Get predictions
    with torch.no_grad():
        output = loaded_model(input_ids, attention_mask)

    # Convert output probabilities to predicted class
    _, predicted_class = torch.max(output, 1)
    predicted_class = predicted_class.detach().cpu().numpy()
    intent = label_decoder[predicted_class[0]].split()
    
    with open('intents.json','r') as json_file:
        data = json.load(json_file)
    for i in data['intents']:
        if i['tag'] == intent[0]:
            result = random.choice(i['responses'])
            break
    # return "\nIntent: "+ intent[0] + '\n' + "Response: " + result
    return intent[0],result


if __name__ == '__main__':
    while True:
        sentence = input("Enter a sentence: ")
        print(classify_intent(sentence))