<template>
  <div class="main">
    <div class="left">
      <LeftMenu class="LeftMenu"
                :trace_list="traceList"
                :unlabeled_trace_list="unlabeledTraceList"
                :selectedTraceId="selectedTraceId"
                @transfer="getSelectedTraceId"></LeftMenu>
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
import { gettracelist } from '@/api/trace.js'
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
    getTracelist () {
      gettracelist().then((res) => {
        this.traceList = res.data
      })
    },
    getSelectedTraceId (msg) {
      this.selectedTraceId = msg
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
  mounted () {
    this.getTracelist()
  }
}
</script>

<style scoped>
.main {
  display: flex;
}
.left {
  width: 20%;
  height: 100vh;
}
.right {
  width: 80%;
  height: 100vh;
  justify-content: space-between;
}
.LeftMenu {
  height: 100%;
}
.topology {
  border: 1px rgb(147, 145, 145) solid;
  height: 42vh;
  width: 100%;
  border-radius: 20px;
  margin: 1em;
  /* width: 100%; */
}
</style>
