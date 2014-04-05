from documents.summary import Summary
from documents.clustering import ClusterMaker


def summarize(cluster, index):
    summary = Summary()

    cluster_maker = ClusterMaker(index)
    sentences = []
    for doc in cluster:
        for sentence in doc.sentences():
            cluster_maker.add(sentence)
            sentences.append(sentence)

    cluster_maker.process_add_list()
    for i in range(5):
        cluster_maker.iterate_affinity()

    representative_sentences = {}
    for sentence in sentences:
        if not sentence.exemplar in representative_sentences:
            representative_sentences[sentence.exemplar] = True

    summary.sentences = representative_sentences.keys()
    summary.guid = cluster[0].guid
    summary.title = cluster[0].title
    summary.publish_date = cluster[0].publish_date

    return summary