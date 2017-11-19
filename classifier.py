import tensorflow as tf, sys

def is_hotdog(img):
    label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]

    res = False
    with tf.gfile.FastGFile("retrained_graph.pb", "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name="")
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name("final_result:0")

        predictions = sess.run(softmax_tensor, {"DecodeJpeg/contents:0":img})

        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print("{} has a score of {}".format(human_string, score));

            if human_string == "hotdogs" and score > 0.8:
                res = True
                                                
    return res


if __name__ == "__main__":
    is_hotdog(tf.gfile.FastGFile(sys.argv[1], "rb").read())
