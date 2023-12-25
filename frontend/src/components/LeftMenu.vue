<template>

  <div class="left-container">
    <div class="left-image-box"><img class="left-image"
           src="../assets/nku.png"
           alt=""></div>
    <div class="menu-box">
      <div class="menu-item">
        <div @click="chosedEmun3=!chosedEmun3"
             class="menu-item-tag">
          <div><i class="el-icon-s-finance"></i>
            <span>List of faulty Traces</span>
          </div>
          <img class="menu-chosed-icon"
               :src="chosedEmun3?upImage:downImage"
               alt="">
        </div>
        <div class="sub-enmu-box"
             v-if="chosedEmun3">
             <div v-for="(item, index) in trace_list" :key="index" :class="activeEmun==index?'sub-enmu-item active-item':'sub-enmu-item'" @click="choseSelectedTraceId(item,index)">Trace {{item}}</div>

        </div>
      </div>

      <div class="menu-item">
        <div @click="chosedEmun2=!chosedEmun2"
             class="menu-item-tag">
          <div><i class="el-icon-discover"></i>
            <span>List of faulty Traces</span>
          </div>
          <img class="menu-chosed-icon"
               :src="chosedEmun2?upImage:downImage"
               alt="">
        </div>
        <div class="sub-enmu-box"
             v-if="chosedEmun2">
          <div :class="activeEmun==2?'sub-enmu-item active-item':'sub-enmu-item'"
               @click="activeEmun=2">Trace 5</div>
          <div :class="activeEmun==3?'sub-enmu-item active-item':'sub-enmu-item'"
               @click="activeEmun=3">Trace 6</div>
          <div :class="activeEmun==4?'sub-enmu-item active-item':'sub-enmu-item'"
               @click="activeEmun=4">Trace 7</div>
        </div>

      </div>

    </div>
  </div>

</template>

<script>

import upward from '../assets/upward.svg'
import downward from '../assets/downward.svg'

export default {
  props: {
    trace_list: []
  },
  name: 'Manage',
  data () {
    return {
      upImage: upward,
      downImage: downward,
      activeEmun: -1,
      chosedEmun2: false,
      chosedEmun3: false

    }
  },
  components: {},
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    choseSelectedTraceId (Traceid, index) {
      this.activeEmun = index
      this.$emit('transfer', Traceid)// 触发transfer方法 为向父组件传递的数据
    }

  },
  mounted () {

  }
}
</script>

<style>
.left-container {
  color: rgba(255, 255, 255, 1);
  background-color: rgba(0, 33, 64, 1);
  font-size: 1.2em;
}

.left-image {
  width: 90%;
  margin: 15px 0;
}
.left-image-box {
  width: 100%;
  height: 10vh;
  background-color: rgba(0, 33, 64, 1);
  margin-bottom: 2em;
}
.menu-box{
    margin-top: 70px;
}
.menu-item {
  padding-top: 7px;
  padding-bottom: 7px;
  text-align: left;
}
.menu-chosed-icon {
  display: inline;
  width: 20px;
  height: 25px;
  margin-right: 20px;
}

.sub-enmu-box {
  padding-top: 15px;
}
.sub-enmu-item {
  padding-bottom: 0.6em;
  padding-left: 60px;
}
.active-item {
  background-color: rgb(2, 34, 63);
  border-color: rgb(2, 34, 63);
  color: rgba(24, 144, 255, 1);
}
.menu-item-tag {
  padding-left: 30px;
  display: flex;
  justify-content: space-between;
}
.menu-item:hover {
  cursor: pointer;
}
.menu-item-tag div span {
  margin-left: 1em;
}
</style>
