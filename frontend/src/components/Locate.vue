<template>
  <div class="main">
    <div class="left">
      <LeftMenu class="LeftMenu"></LeftMenu>
    </div>

  
  <div class="right">
    <div class="right-top">
      <Microservice class="microservice"></Microservice>
    </div>
    
    <div class="right-bottom">
      <div class="options">
        <select v-model="selectedOption" class="select-box">
          <option value="1h">1h</option>
          <option value="2h">2h</option>
          <option value="5h">5h</option>
          <option value="10h">10h</option>
        </select>
        <button @click="confirmSelection" class="confirm-button">确认选择</button>
      </div>
    </div>
  </div>
</div> 
</template>

<script>
import LeftMenu from '@/components/LeftMenu.vue'
import Microservice from './Microservice.vue'


export default {
  components: {
    LeftMenu,
    Microservice
  },
  data () {
    return {
      selectedOption: '1h' // 默认选择1小时
    }
  },
  methods: {
    confirmSelection() {
      // 处理确认选择的逻辑
      
      console.log('确认选择:', this.selectedOption);
    },

  },
  created () {

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
  width: 21%;
  height: 100%;
}
.LeftMenu {
  height: 100%;
}
.right {
  width: 78%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-color: white;
}
.right-top {
  width: 100%;
  height: 78%;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
}

.right-bottom {
  width: 100%;
  height: 19%;
  overflow-y: auto;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
}
.options {
  width: 100%;
  height: 40%;
}
.select-box {
  width: 120px; /* 增加选择框宽度 */
  height: 40px; /* 增加选择框高度 */
  padding: 5px; /* 增加内边距 */
}
.confirm-button {
  width: 120px; /* 将宽度修改为您需要的值 */
  height: 40px;
  color: white;
  background-color:rgba(0, 33, 64, 1);
  border-color: rgba(0, 33, 64, 1);
  border-radius: 5px;
}


</style>
