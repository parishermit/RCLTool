<template>
  <div class="main">
    <div class="left">
      <LeftMenu class="LeftMenu"
                :traceList="traceList"
                :unlabeled_trace_list="unlabeledTraceList"
                @trace-selected="handleTraceSelected"></LeftMenu>
    </div>

    <div class="right">
      <div class="right-top">
        <Topology class="topology"
                  :id="selectedTraceId"
                  @transfer="labelSuccessfully"></Topology>
      </div>
      <div class="right-bottom">
        <trace-graph :id="selectedTraceId" />
      </div>
    </div>

  </div>
</template>

<script>
import LeftMenu from '@/components/LeftMenu.vue'
import Topology from '@/components/Topology.vue'
import TraceGraph from '@/components/TraceGraph/index.vue'
import { getTraceList } from '@/api/trace.js'

export default {
  components: {
    LeftMenu,
    Topology,
    TraceGraph
  },
  data () {
    return {
      traceList: [],
      unlabeledTraceList: [],
      selectedTraceId: ''
    }
  },
  methods: {
    getTraceList () {
      return new Promise((resolve, reject) => {
        getTraceList().then((res) => {
          this.traceList = res.data
          resolve() // 解决 Promise
          // 进行其他操作，如果需要的话
        }).catch((error) => {
          reject(error) // 拒绝 Promise
        })
      })
    },
    handleTraceSelected (selectedTraceId) {
      this.selectedTraceId = selectedTraceId
      console.log('home select trace id', selectedTraceId)
    },
    labelSuccessfully (labeledTraceId) {
      for (let i = this.traceList.length - 1; i >= 0; i--) {
        if (this.traceList[i] === labeledTraceId) {
          this.unlabeledTraceList.push(this.traceList.splice(i, 1)[0])
          if (this.traceList.length > 0) {
            this.selectedTraceId =
              this.traceList[Math.floor(Math.random() * this.traceList.length)]
          } else this.selectedTraceId = -1
          break
        }
      }
    }
  },
  created () {
    this.getTraceList().then(() => {
      console.log('tracelist', this.traceList) // 输出 testList 值
    }).catch((error) => {
      console.error('Error while fetching data:', error)
    })
  }
}
</script>

<style scoped>
.main {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 96vh;
  margin: 0;
  padding: 0;
}
.left {
  width: 20%;
  height: 100%;
}
.LeftMenu {
  height: 100%;
}
.right {
  width: 79%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.right-top {
  width: 100%;
  height: 48%;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
}
.topology {
  height: 100%;
  width: 100%;
}
.right-bottom {
  width: 100%;
  height: 48%;
  overflow-y: auto;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
}
</style>
