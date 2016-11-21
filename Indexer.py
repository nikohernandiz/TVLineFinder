
#Indexer assumes that collection fits in memory
class Indexer(object):
	def __init__(self):
		self.inverted_index = dict()
		self.forward_index = dict()
		self.url_to_id = dict()	
		self.doc_count = 0			

	#assumes that add_document() is never called twice for a document
	# assumes that a document has a unique URL
	def add_document(self,url, parsed_text):
		self.doc_count +=1
		assert url not in self.url_to_id
		current_id = self.doc_count
		self.forward_index[current_id] = parsed_text
		for word in parsed_text:
			if word not in self.inverted_index:
				self.inverted_index[word] = []
			self.inverted_index[word].append(current_id)
	
	def store_on_disk(self, index_dir):
		inverted_index_file_name = os.path.join(index_dir, "inverted_index")
		forward_index_file_name  = os.path.join(index_dir, "forward_index")
		inverted_index_file = open(inverted_index_file_name, "w")
		forward_index_file_name = open(forward_index_file_name, "w")	
		json.dump(self.inverted_index, inverted_index_file)
		json.dump(self.forward_index, forward_index_file)

	
def main():
	parser = argparse.ArgumentParser(description='Index https://www.reddit.com/r/learnprogramming/')
	parser.add_argument("--stored_documents", dest = "stored_documents")
	parser.add_argument("--index_dir", dest = index_dir")
	args = parser.parse_args()
	
		
#are we involing this from cli
if __name__ == "__main__": 
	main()
	
