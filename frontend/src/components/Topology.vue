<template>
  <div class="topology-main">
    <div ref="network" class="topomap">


    </div>
    <div style="position: absolute;top: 20px;left: 20px;">Topological Relationship Diagram</div>
    <div style="position: absolute;top: 20px;left: 0px;width: 2px;background-color: rgb(89,163,253);">&nbsp;</div>
    <div class="button-box">
      <el-button type="primary" @click="Normal" size="mini" round>Normal</el-button>
      <el-button type="primary" @click="Abnormal" size="mini" round>Abnormal</el-button>
    </div>

    <div id="customTooltip" class="custom-tooltip"></div>
  </div>
</template>

<script>
import { Network } from 'vis'
import { getNodesAndEdges, abnormalLabelRequest } from '@/api/trace.js'
export default {
  props: {
    id: String
  },
  data() {
    return {
      nodes: [],
      edges: [],
      //   nodes: [
      //     { id: 'asd', label: 'Service 1', shape: 'circle' },
      //     { id: 'zxc', label: 'Service 2', shape: 'circle' },
      //     { id: 'qwe', label: 'Service 3', shape: 'circle' },
      //     { id: '123', label: 'Service 4', shape: 'circle' },
      //     { id: '456', label: 'Service 5', shape: 'circle', color: 'red' }
      //   ],
      //   edges: [
      //     { from: 'asd', to: 'zxc' },
      //     { from: 'zxc', to: 'qwe' },
      //     { from: 'zxc', to: '456' },
      //     { from: '456', to: '123' }
      //   ],
      radio: -1,
      selectedNodeId: '',
      dialogVisible: false
    }
  },
  methods: {
    Normal(){
      this.$emit('update-type', "Normal");
      this.$emit('update-value', Date.now()+","+this.id);
    },
    Abnormal(){
      this.$emit('update-type', "Abnormal");
      this.$emit('update-value', Date.now()+","+this.id);
    },
    createTopology() {
      {
        // 创建拓扑图
        const container = this.$refs.network
        const data = {
          nodes: this.nodes,
          edges: this.edges
        }

        // 根据需要设置图形的选项
        const options = {
          // zoom: 5,
          // 节点样式
          nodes: {
            size: 1000,
            borderWidth: 2,
            color: {},
          },
          // 连接线的样式
          edges: {
            color: {
              color: 'rgb(97, 168, 224)',
              highlight: 'rgb(97, 168, 224)',
              hover: 'red',
              inherit: 'from',
              opacity: 1.0
            },
            font: {
              align: 'top' // 连接线的样式
            },
            smooth: true, // 是否显示方向箭头
            arrows: { to: true } // 箭头指向from节点
          },
          // layout: { randomSeed: 20 },
          interaction: {
            navigationButtons: true,
            hover: true, // 鼠标移过后加粗该节点和连接线
            selectConnectedEdges: false // 选择节点后是否显示连接线
          },
          manipulation: {
            enabled: false
          }
        }

        const network = new Network(container, data, options)

        // 添加点击节点事件监听器
        network.on('doubleClick', (event) => {
          const { nodes } = event
          if (nodes.length > 0) {
            const nodeId = nodes[0]
            this.showSelectionDialog(nodeId)
          }
        })
        // 添加事件监听器
        network.on('click', function (params) {
          // 鼠标悬停在节点上时的事件处理
          const { nodes } = params
          if (nodes.length > 0) {
            var nodeId = nodes[0]
            var nodeDetails
            for (let i = 0; i < data.nodes.length; i++) {
              if (data.nodes[i].id === nodeId) {
                nodeDetails = data.nodes[i]
                break
              }
            }

            // 获取悬浮框元素
            var customTooltip = document.getElementById('customTooltip')

            // 设置悬浮框内容和位置
            customTooltip.innerHTML =
              'Time latency is ' + nodeDetails['duration'] + 'ms'
            customTooltip.style.left = params.pointer.DOM.x + 10 + 'px'
            customTooltip.style.top = params.pointer.DOM.y - 10 + 'px'

            // 显示悬浮框
            customTooltip.style.display = 'block'
          }
        })

        network.on('blurNode', function () {
          // 鼠标移出节点时的事件处理
          // 隐藏悬浮框
          var customTooltip = document.getElementById('customTooltip')
          customTooltip.style.display = 'none'
        })
      }
    },
    showSelectionDialog(nodeId) {
      this.selectedNodeId = nodeId
      this.dialogVisible = true
    },
    getSpanList() {
      return new Promise((resolve, reject) => {
        getNodesAndEdges({ trace_id: this.id })
          .then((res) => {
            this.nodes = res.data[0]
            this.edges = res.data[1]
            resolve() // 解决 Promise
            // 进行其他操作，如果需要的话
          })
          .catch((error) => {
            reject(error) // 拒绝 Promise
          })
      })
    },
    abnormalLabel() {
      abnormalLabelRequest({
        trace_id: this.id,
        span_id: this.selectedNodeId
      }).then((res) => {
        this.next()
      })
    },
    next() {
      this.dialogVisible = false
      this.radio = -1
      this.$emit('transfer', this.id) // 触发transfer方法 为向父组件传递的数据
    }
  },
  mounted() {
    this.getSpanList()
      .then(() => {
        this.createTopology() // testList 值
      })
      .catch((error) => {
        console.error('Error while fetching data:', error)
      })
  },
  watch: {
    id() {
      this.getSpanList()
        .then(() => {
          this.createTopology()
        })
        .catch((error) => {
          console.error('Error while fetching data:', error)
        })
    }
  }
}
</script>

<style scoped>
.topology-main {
  position: relative;
  width: 100%;
  height: 100%;
}

.topomap {
  width: 100%;
  height: 100%;
  position: relative;
}

.button-box {
  /* width: 15%;
  height: 40px; */
  position: absolute;
  bottom: 1em;
  right: 1em;
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
}

.button-box button {
  margin-right: 1rem;
}

.dialog-box div {
  margin: 15px;
}

/* 悬浮框的样式 */
.custom-tooltip {
  position: absolute;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  display: none;
}
</style>
