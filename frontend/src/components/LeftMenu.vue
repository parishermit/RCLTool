<template>

  <div class="left-container">
    <div class="left-image-box">
      <img class="left-image" src="../assets/nku.png" alt="">
    </div>
    <div class="menu-box">
      <div class="menu-item"
        v-for="(traceId, index) in traceList"
        :key="index"
        @click="setSelectedTraceId(traceId)">
        <div>
          <span>{{ traceId }}</span>
        </div>
      </div>
    </div>
    <div class="upload">
      <input type="file" ref="fileInput" style="display: none" @change="handleFileUpload">
      <el-button type="primary" @click="chooseFile">选择文件</el-button>
      <el-button type="primary" @click="uploadFile">上传</el-button>
    </div>
    <div class="export">
      <el-button type="primary" @click="downloadGroundtruthCsv">导出groundtruth</el-button>
      <el-button type="primary" @click="downloadTraceCsv">导出trace</el-button>
    </div>
  </div>

</template>

<script>
import upward from '../assets/upward.svg'
import downward from '../assets/downward.svg'
import { uploadData, downloadGroundtruth, downloadTrace } from '../api/trace.js'
export default {
  props: {
    traceList: [],
    unlabeled_trace_list: []
  },
  name: 'Manage',
  data () {
    return {
      upImage: upward,
      downImage: downward,
      selectedTraceId: '',
      fileToUpload: null
    }
  },
  components: {},
  mounted () {
    console.log('leftmenu mounted', this.traceList)
    this.selectedTraceId = this.traceList[0]
  },
  methods: {
    setSelectedTraceId (id) {
      this.selectedTraceId = id
      console.log('select id', this.selectedTraceId)
      this.$emit('trace-selected', id)
    },
    chooseFile () {
      this.$refs.fileInput.click()
    },
    handleFileUpload (event) {
      const file = event.target.files[0]
      if (file) {
        // 获取上传文件名
        const fileName = file.name
        // 检查文件名是否为 "trace.csv"
        if (fileName === 'trace.csv') {
          // 文件名合法，可以进行上传操作
          this.fileToUpload = file
          alert('文件选择成功！')
        } else {
          // 文件名不符合要求，给出提示或者阻止上传
          alert('请上传名为 "trace.csv" 的文件')
          this.$refs.fileInput.value = '' // 清空文件输入框
        }
      }
    },
    uploadFile () {
      // 处理上传文件的逻辑
      if (this.fileToUpload) {
        // 执行上传操作
        const formData = new FormData()
        formData.append('trace.csv', this.fileToUpload)

        uploadData(formData)
          .then(response => {
            // 处理后端返回的数据
            console.log(response)
            alert('文件上传成功！')
            location.reload()
          })
          .catch(error => {
            // 处理错误
            console.error('文件上传失败：', error)
            alert('文件上传失败！')
          })
      } else {
        alert('请选择一个文件进行上传')
      }
    },
    downloadTraceCsv () {
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
    downloadGroundtruthCsv () {
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
.left-container {
  height: 100%;
  color: rgba(255, 255, 255, 1);
  background-color: rgba(0, 33, 64, 1);
  font-size: 1.2em;
}

.left-image-box {
  width: 100%;
  height: 15%;
  background-color: rgba(0, 33, 64, 1);
}
.left-image {
  width: 90%;
  margin: 15px 0;
}
.menu-box{
  width: 100%;
  height: 65%;
  overflow-y: auto;
}
.menu-item {
  height: 8vh;
  width: 100%;
  background-color: rgb(54, 90, 123);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.upload {
  height: 10%;
  width: 100%;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  align-items: center;
}
.export {
  height: 10%;
  width: 100%;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  align-items: center;
}
.left-bottom button {
  height: 40px;
}
</style>
