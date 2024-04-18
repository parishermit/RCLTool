<template>
  <div class="left-container">
    <!-- <div class="left-image-box">
      <img class="left-image" src="../assets/logo.png" alt="">
    </div> -->
    <div style="display: flex;margin: 10px 0;">
      <div style="width: 2px;background-color: rgb(88,162,252);"></div>
      <div style="color: black; font-size: 16px;">&nbsp;&nbsp;&nbsp;Task</div>
    </div>

    <div style="display: flex;margin: 24px 0;align-items: center;">
      <div style="color: #516571; font-size: 16px;margin-right: 25px;">&nbsp;&nbsp;&nbsp;&nbsp;Select task</div>
      <select v-model="selectedTask" style="width: 120px; height: 30px; border-radius: 10px; padding: 5px;">
        <!-- <option v-for="(task, index) in taskList" :key="index" :value="task.task_id">{{ task.task_id + ' ' + task.task_name }}</option> -->
        <option value="a">Task 1</option>
        <option value="b">Task 2</option>
        <option value="c">Task 3</option>
      </select>
    </div>

    <div class="menu-box">
      <div style="display: flex;margin: 10px 0;">
        <div style="width: 2px;background-color: rgb(88,162,252);"></div>
        <div style="color: black; font-size: 16px;">&nbsp;&nbsp;&nbsp;Trace List</div>

      </div>
      <div class="menu-item" v-for="(traceId, index) in traceList" :key="index" @click="setSelectedTraceId(traceId)">
        <div style="display: flex;justify-content:center">
          <div class="" style="width: 100px; white-space: nowrap; overflow: hidden;" :class="getClass(traceId)" >{{ traceId }}</div>
        </div>
      </div>
    </div>
    <div class="upload">
      <el-button type="primary" size="mini" @click="downloadTraceCsv" round style="margin-top: 10%;"> Export trace </el-button>
    </div>

    <!-- <div class="export">
      <el-button type="primary" size="mini" @click="downloadGroundtruthCsv" round>导出groundtruth</el-button>
    </div> -->
  </div>

</template>

<script>
import upward from '../assets/upward.svg'
import downward from '../assets/downward.svg'
import { uploadData, downloadGroundtruth, downloadTrace } from '../api/trace.js'
export default {
  props: {
    traceList: [],
    unlabeled_trace_list: [],
    sharedValue: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: ''
    },
  },
  name: 'Manage',
  data() {
    return {
      upImage: upward,
      downImage: downward,
      selectedTraceId: '',
      fileToUpload: null,
      id_list : {},
    }
  },
  components: {},
  mounted() {
    console.log('leftmenu mounted', this.traceList)
    this.selectedTraceId = this.traceList[0]
  },
  watch: {
    sharedValue(newVal){
      let arr = newVal.split(",");
      console.log('arr=>'+ arr[1] )
      // this.id_list[arr[1]] = this.type
      this.$set(this.id_list, arr[1], this.type)
      // this.id_list.push(newVal)
      // const mySet = new Set(this.id_list);
      // const uniqueArray = Array.from(mySet);
      // this.id_list = uniqueArray
      console.log('sharedValue=>'+ newVal )
      console.log('type=>'+ this.type )
      console.log(this.id_list)
    },
    id (newVal) {

      
      console.log('new'+ newVal )
      this.selectedTraceId = newVal;
      this.fetchList(newVal)
    }
  },
  methods: {
    getClass(traceId) {
    return this.id_list[traceId] === 'Abnormal' ? 'text-red' :
           this.id_list[traceId] === 'Normal' ? 'text-green' : '';
  },
    SetValue() {
      console.log(1);
    },
    setSelectedTraceId(id) {
      this.selectedTraceId = id
      console.log('select id', this.selectedTraceId)
      this.$emit('trace-selected', id)
      console.log(this.id_list)
    },
    chooseFile() {
      this.$refs.fileInput.click()
    },

    downloadTraceCsv() {
      downloadTrace().then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'trace.csv') // 文件名可以根据后端的响应来设置
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }).catch(error => {
        console.error('下载失败:', error)
      })
    },
    downloadGroundtruthCsv() {
      downloadGroundtruth().then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'groundtruth.csv') // 文件名可以根据后端的响应来设置
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }).catch(error => {
        console.error('下载失败:', error)
      })
    }
  }
}
</script>

<style>
.text-red{
  color: red;
}
.text-green{
  color: green;
}
.left-container {
  height: 80hv;
  color: rgba(255, 255, 255, 1);
  /* background-color: white; */
  font-size: 1.2em;
  border-radius: 8px;
}

.left-image-box {
  width: 75%;
  height: 15%;
  background-color: white;
}

.left-image {
  width: 90%;
  margin: 15px 0;
}

.menu-box {
  width: 100%;
  height: 75%;
  overflow-y: auto;
  overflow-x: hidden;
}

.menu-item {

  width: 100%;
  white-space: nowrap;
  /* 不换行 */
  overflow: hidden;
  /* 溢出部分隐藏 */
  font-size: 15px;
  color: #555555;
  background-color: white;
  max-width: 380px;
  padding: 5px 10px;
  line-height: 25px;
  border-bottom: 1px solid #ccc;
  /* border-bottom: 1px solid rgb(54, 90, 123); */
  /* display: flex;
  align-items: center;
  justify-content: center; */
}

.menu-item:hover {
  background-color: rgb(233, 246, 255);
  border-color: rgb(233, 246, 255)
    /* 悬停时将按钮的背景色修改为灰色 */
}

.upload {
  width: 100%;
  /* display: flex;
  align-items: center; */
  text-align: center;
}

.export {
  /* height: 10%; */
  width: 100%;
  display: flex;

}

.left-bottom button {
  height: 40px;
}

.el-button {}

.el-button:hover {
  background-color: gray;
  border-color: gray
    /* 悬停时将按钮的背景色修改为灰色 */
}
</style>
