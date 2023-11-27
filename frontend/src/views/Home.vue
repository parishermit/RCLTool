<template>
  <div class="main">
    <LeftMenu class="LeftMenu"></LeftMenu>

    <!-- <div class="right-box">

        </div> -->
    <Topology class="topology"></Topology>

  </div>
</template>

<script>
import LeftMenu from '@/components/LeftMenu.vue'
import Topology from '@/components/Topology.vue'

export default {
  components: {
    LeftMenu,
    Topology
  },

  methods: {},
  mounted () {}
}
</script>

<style scoped>
.main {
  display: flex;
}
.right-box {
  /* position: absolute; */
  /* left: 290px; */
  display: flex;
  width: 80%;
  height: 45vh;
  justify-content: space-between;
}
.LeftMenu {
  width: 20%;
  height: 100vh;
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
