<template>
  <div>
    <div ref="network" style="height: 100%; border: 1px #ccc;"></div>

    <el-dialog title="Tip" :visible.sync="dialogVisible" width="30%" center>
      <div class='dialog-box'>
        <div>Please select the fault type:</div>
        <div>
          <el-radio-group v-model="radio">
            <el-radio :label="1" class="radio-item">Time Anomaly</el-radio><br>
            <el-radio :label="2" class="radio-item">Structural Anomaly</el-radio><br>
            <el-radio :label="3" class="radio-item">Network</el-radio><br>
          </el-radio-group>
        </div>

        <div>Determine whether to mark the Trace as an exception?</div>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false" size="mini" round>Cancel</el-button>
        <el-button type="primary" @click="abnormalLabel" size="mini" round>Confirm</el-button>
      </span>
    </el-dialog>

    <div id="customTooltip" class="custom-tooltip"></div>
  </div>



</template>

<script>
import { DataSet, Network } from 'vis'
import { testGetRes } from '../api/trace.js'
import { getNodesAndEdges, abnormalLabelRequest } from '@/api/trace.js'
export default {
  data() {
    return {
      res: "",
      nodes: new DataSet(),
      edges: new DataSet(),
      options: {
        physics: false
      },
      radio: -1,
      selectedNodeId: '',
      dialogVisible: false
    }
  },
  mounted() {
    this.test()
  },
  methods: {
    test() {
      testGetRes({}).then((ans) => {
        // console.log(res)
        this.res = ans.data["1"]
        this.nodes = ans.data["nodes"]
        this.edges = ans.data["edges"]
        console.log(this.edges)
        console.log(this.nodes)
        this.createTopology()
      })
    },
    drawNetwork() {
      const container = this.$refs.network;
      const data = {
        nodes: this.nodes,
        edges: this.edges
      };
      const options = this.options;
      // 创建拓扑图
      console.log('Drawing network with data:', data);
      this.network = new Network(container, data, options);
    },
    createTopology() {
      {
        // 创建拓扑图
        const container = this.$refs.network
        const data = {
          nodes: this.nodes,
          edges: this.edges
        }
        const options = {
          edges: {
            color: {
              color: 'rgb(97, 168, 224)',
              highlight: 'rgb(97, 168, 224)',
              hover: 'blue',
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
        // 添加节点单击事件监听器
        this.network.on('click', (event) => {
          const nodeId = event.nodes[0];
          if (nodeId !== undefined) {
            this.showPopover(nodeId);
          }
        })
      }
    },
    showSelectionDialog(nodeId) {
      this.selectedNodeId = nodeId
      this.dialogVisible = true
    },
    // abnormalLabel() {
    //   abnormalLabelRequest({
    //     trace_id: this.id,
    //     span_id: this.selectedNodeId
    //   }).then((res) => {
    //     this.next()
    //   })
    // },
    // next() {
    //   this.dialogVisible = false
    //   this.radio = -1
    //   this.$emit('transfer', this.id) // 触发transfer方法 为向父组件传递的数据
    // }

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
.radio-item {
  margin-bottom: 13px; 
}
</style>
