import json
import os

def create_inverted_index_from_lemmas_files(directory, output_file):
    inverted_index = {}

    for filename in os.listdir(directory):
        if filename.startswith("lemmas_"):
            filepath = os.path.join(directory, filename)
            doc_id = filename[len("lemmas_"):]
            doc_id = doc_id.removesuffix(".txt")
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    all_text = infile.read()
                    lemmas = all_text.split()

                    for lemma in lemmas:
                        if lemma in inverted_index:
                            inverted_index[lemma].add(doc_id)
                        else:
                            inverted_index[lemma] = {doc_id}

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue

    inverted_index_serializable = {lemma: list(doc_ids) for lemma, doc_ids in inverted_index.items()}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(inverted_index_serializable, outfile, indent=4, ensure_ascii=False)

    print(f"Inverted index saved to {output_file}")


directory = "../out/tokens"
output_file = "../out/inverted_index.json"

create_inverted_index_from_lemmas_files(directory, output_file)

with open(output_file, 'r', encoding='utf-8') as infile:
    loaded_index = json.load(infile)

print("\nLoaded inverted index:")
print(json.dumps(loaded_index, indent=4, ensure_ascii=False))