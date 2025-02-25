"""
    @Project: tensorflow_models_nets
    @File   : convert_pb.py
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2018-08-29 17:46:50
    @info   :
    -通过传入 CKPT 模型的路径得到模型的图和变量数据
    -通过 import_meta_graph 导入模型中的图
    -通过 saver.restore 从模型中恢复图中各个变量的数据
    -通过 graph_util.convert_variables_to_constants 将模型持久化
"""

import tensorflow as tf
from tensorflow.python.framework import graph_util


def freeze_graph(model_folder, output_graph):
    '''
    :param input_checkpoint:
    :param output_graph: PB模型保存路径
    :return:
    '''
    checkpoint = tf.train.get_checkpoint_state(model_folder)  # 检查目录下ckpt文件状态是否可用
    input_checkpoint = checkpoint.model_checkpoint_path  # 得ckpt文件路径

    # 指定输出的节点名称,该节点名称必须是原模型中存在的节点
    output_node_names = "loss/ReverseSequence_1"
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)

    with tf.Session() as sess:
        saver.restore(sess, input_checkpoint)  # 恢复图并得到数据
        output_graph_def = graph_util.convert_variables_to_constants(  # 模型持久化，将变量值固定
            sess=sess,
            input_graph_def=sess.graph_def,  # 等于:sess.graph_def
            output_node_names=output_node_names.split(","))  # 如果有多个输出节点，以逗号隔开

        with tf.gfile.GFile(output_graph, "wb") as f:  # 保存模型
            f.write(output_graph_def.SerializeToString())  # 序列化输出
        print("%d ops in the final graph." % len(output_graph_def.node))  # 得到当前图有几个操作节点

        # for op in sess.graph.get_operations():
        #     print(op.name, op.values())


def freeze_graph2(input_checkpoint, output_graph):
    '''
    :param input_checkpoint:
    :param output_graph: PB模型保存路径
    :return:
    '''
    # checkpoint = tf.train.get_checkpoint_state(model_folder) #检查目录下ckpt文件状态是否可用
    # input_checkpoint = checkpoint.model_checkpoint_path #得ckpt文件路径

    # 指定输出的节点名称,该节点名称必须是原模型中存在的节点
    output_node_names = "InceptionV3/Logits/SpatialSqueeze"
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)
    graph = tf.get_default_graph()  # 获得默认的图
    input_graph_def = graph.as_graph_def()  # 返回一个序列化的图代表当前的图

    with tf.Session() as sess:
        saver.restore(sess, input_checkpoint)  # 恢复图并得到数据
        output_graph_def = graph_util.convert_variables_to_constants(  # 模型持久化，将变量值固定
            sess=sess,
            input_graph_def=input_graph_def,  # 等于:sess.graph_def
            output_node_names=output_node_names.split(","))  # 如果有多个输出节点，以逗号隔开

        with tf.gfile.GFile(output_graph, "wb") as f:  # 保存模型
            f.write(output_graph_def.SerializeToString())  # 序列化输出
        print("%d ops in the final graph." % len(output_graph_def.node))  # 得到当前图有几个操作节点

        # for op in graph.get_operations():
        #     print(op.name, op.values())


if __name__ == '__main__':
    # 输入ckpt模型路径
    model_folder = 'ner_bert_base'
    # 输出pb模型的路径
    out_pb_path = "pb/frozen_model.pb"
    # 调用freeze_graph将ckpt转为pb
    freeze_graph(model_folder, out_pb_path)
