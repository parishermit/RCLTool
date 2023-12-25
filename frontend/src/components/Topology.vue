<template>
  <div class="topology-main">
    <div ref="network"
         class="topomap"></div>
    <div class="button-box">
      <el-button type="primary">Annotate Anomaly</el-button>
      <el-button type="primary">Annotate Root Cause</el-button>
    </div>
    <el-dialog title="Tip"
               :visible.sync="dialogVisible"
               width="30%"
               center>
      <span>Determine whether to mark the Trace as an exception?</span>
      <span slot="footer"
            class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary"
                   @click="abnormalLabel">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { Network } from 'vis'
import { getNodesAndEdges, abnormalLabelRequest } from '@/api/trace.js'
export default {
  props: {
    id: String
  },
  data () {
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
      selectedNodeId: '',
      dialogVisible: false
    }
  },
  methods: {
    createTopology () {
      {
        // 创建拓扑图
        const container = this.$refs.network
        const data = {
          nodes: this.nodes,
          edges: this.edges
        }

        // const options = {}; // 根据需要设置图形的选项
        const options = {
          // zoom: 5,
          // 节点样式
          // nodes: {
          //   size: 60,
          //   borderWidth: 2,
          //   color: {},
          // },
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
        network.on('click', (event) => {
          const { nodes } = event
          if (nodes.length > 0) {
            const nodeId = nodes[0]
            this.showSelectionDialog(nodeId)
            // console.log(`Node ${nodeId} clicked`);
            // 在这里可以执行点击节点后的操作
          }
        })
      }
    },
    showSelectionDialog (nodeId) {
      this.selectedNodeId = nodeId
      this.dialogVisible = true
    },
    getSpanList () {
      return new Promise((resolve, reject) => {
        getNodesAndEdges({ trace_id: this.id }).then((res) => {
          this.nodes = res.data[0]
          this.edges = res.data[1]
          resolve() // 解决 Promise
          // 进行其他操作，如果需要的话
        }).catch((error) => {
          reject(error) // 拒绝 Promise
        })
      })
    },
    abnormalLabel () {
      abnormalLabelRequest({trace_id: this.id, span_id: this.selectedNodeId}).then((res) => {
        alert(1)
        this.dialogVisible = false
      })
    }
  },
  mounted () {
    this.getSpanList().then(() => {
      this.createTopology()// testList 值
    }).catch((error) => {
      console.error('Error while fetching data:', error)
    })
  },
  watch: {
    id () {
      console.log('id changed')
      this.getSpanList().then(() => {
        this.createTopology()
      }).catch((error) => {
        console.error('Error while fetching data:', error)
      })
    }
  }
}
</script>

<style scoped>
.topology-main {
  position: relative;
}
.topomap {
  height: 100%;
}
.button-box {
  width: 15%;
  height: 40px;
  position: absolute;
  bottom: 1em;
  right: 1em;
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
}
.button-box button{
    margin-right: 1rem;
}
</style>
