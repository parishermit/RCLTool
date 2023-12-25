<template>
  <div class="main">
    <div class="left" @click="changeTraceId">
      <LeftMenu class="LeftMenu"></LeftMenu>
    </div>

    <div class="right">
      <div class="right-top">
        <Topology class="topology" :id="selectedTraceId"></Topology>
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

export default {
  components: {
    LeftMenu,
    Topology,
    TraceGraph
  },
  data () {
    return {
      traceList: [],
      selectedTraceId: '1234'
    }
  },
  methods: {
    changeTraceId () {
      this.selectedTraceId = '1234'
      console.log(this.selectedTraceId)
    }
  },
  mounted () {}
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
