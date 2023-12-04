<template>
  <div class="list">
    <div class="head">
      <div class="label-pod-list">
        <label-pod v-for="(pod, index) in podList"
                    :key="index"
                    :content="pod"
                    :color="getPodColor(index)"></label-pod>
      </div>
      <el-button type="primary"
                  @click="handleImageExport()">导出为图片</el-button>
    </div>
    <div class="main"
          ref="main">
      <svg version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="100%"
            height="100%"
            style="position: absolute; z-index: 1">
        <path v-for="(span, index) in spanList"
              :key="index"
              fill="rgba(0,0,0,0)"
              stroke="rgba(0, 0, 0, 0.1)"
              stroke-width="2"
              transform="translate(5, 0)"
              :d="getPath(span)"></path>
      </svg>
      <div class="span-list">
        <el-tooltip effect="dark"
                    content="ROOT"
                    placement="top">
          <div class="root">
            <div class="dot"></div>
            <trace-graph-ruler :length="totalDuration"
                                class="right"></trace-graph-ruler>
          </div>
        </el-tooltip>
        <template v-for="(span, index) in spanList">
          <el-tooltip effect="dark"
                      placement="top"
                      :key="index">
            <div slot="content">
              {{ span.operationName }}<br /><br />Duration: {{ span.duration }}
            </div>
            <div class="span"
                  :style="{ 'margin-left': span.deep * 12 + 'px' }">
              <div class="span-left">
                <div class="dot"
                      :style="{ 'background-color': getSpanColor(span) }"></div>
                <img :src="require('../../assets/' + span.type + '.png')"
                      class="image" />
                <div class="error"
                      v-if="span.statusCode !== 200 && span.statusCode !== 0"></div>
                <div>
                  <div style="color: #2c3e50">{{ span.operationName }}</div>
                  <div style="color: #d4d4d4">{{ span.cmdbId }}</div>
                </div>
              </div>
              <div class="pillar"
                    :style="{
                  'background-color': getSpanColor(span),
                  width: (span.duration / totalDuration) * 350 + 'px',
                  'margin-right':
                    ((endTime - span.duration - span.timestamp) /
                      totalDuration) *
                      350 +
                    15 +
                    'px',
                }"></div>
            </div>
          </el-tooltip>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import LabelPod from '@/components/Label/pod.vue'
import TraceGraphRuler from '@/components/TraceGraph/ruler.vue'
import html2canvas from 'html2canvas'

export default {
  name: 'TraceGraphList',
  components: {
    LabelPod,
    TraceGraphRuler
  },
  props: {
    spanList: Array
  },
  data () {
    return {
      podList: [],
      totalDuration: 0,
      endTime: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      this.podList = []
      this.endTime = 0
      var startTime = this.spanList[0].timestamp
      this.spanList.forEach((item) => {
        if (this.podList.indexOf(item.cmdbId) === -1) {
          this.podList.push(item.cmdbId)
        }
        if (item.timestamp < startTime) {
          startTime = item.timestamp
        }
        if (item.duration + item.timestamp > this.endTime) {
          this.endTime = item.duration + item.timestamp
        }
        var deep = 1
        var tempSpan = item
        while (tempSpan.parentSpan !== null && tempSpan.parentSpan !== undefined && tempSpan.parentSpan !== '') {
          tempSpan = this.spanList.find(
            (span) => span.spanId === tempSpan.parentSpan
          )
          deep++
        }
        item.deep = deep
      })
      this.totalDuration = this.endTime - startTime
      console.log('list.vue', this.spanList)
    },
    getPodColor (index) {
      var length = this.podList.length
      var start = {
        r: 110,
        g: 64,
        b: 170
      }
      var end = {
        r: 52,
        g: 240,
        b: 126
      }
      if (length === 1) {
        return 'rgb(' + start.r + ', ' + start.g + ', ' + start.b + ')'
      } else {
        var color = {}
        color.r = ((end.r - start.r) / (length - 1)) * index + start.r
        color.g = ((end.g - start.g) / (length - 1)) * index + start.g
        color.b = ((end.b - start.b) / (length - 1)) * index + start.b
        return 'rgb(' + color.r + ', ' + color.g + ', ' + color.b + ')'
      }
    },
    getSpanColor (span) {
      return this.getPodColor(
        this.podList.findIndex((pod) => pod === span.cmdbId)
      )
    },
    getPath (span) {
      var startPosition = {}
      if (span.parentSpan === '' || span.parentSpan === null || span.parentSpan === undefined) {
        startPosition = {
          x: -2,
          y: 25
        }
      } else {
        var parentIndex = this.spanList.findIndex(
          (item) => item.spanId === span.parentSpan
        )
        startPosition = {
          x: -2 + this.spanList[parentIndex].deep * 13,
          y: 25 + (parentIndex + 1) * 52
        }
      }
      var endPosition = {
        x: -2 + span.deep * 13,
        y:
          20 +
          (this.spanList.findIndex((item) => item.spanId === span.spanId) + 1) *
            52
      }
      return (
        'M ' +
        String(startPosition.x) +
        ' ' +
        String(startPosition.y) +
        ' L ' +
        String(startPosition.x) +
        ' ' +
        String(endPosition.y - 25) +
        ' L ' +
        String(endPosition.x) +
        ' ' +
        String(endPosition.y - 15) +
        ' L ' +
        String(endPosition.x) +
        ' ' +
        String(endPosition.y)
      )
    },
    handleImageExport () {
      html2canvas(this.$refs.main).then((canvas) => {
        const el = document.createElement('a')
        el.href = canvas.toDataURL('image/png')
        el.download = 'image'
        const event = new MouseEvent('click')
        el.dispatchEvent(event)
      })
    }
  },
  watch: {
    spanList () {
      this.getData()
    }
  }
}
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 10px;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.label-pod-list {
  display: flex;
  flex-wrap: wrap;
}

.el-button {
  height: 24px;
  padding: 2px 10px;
  font-size: 12px;
}

.main {
  position: relative;
  flex-flow: 1;
  height: 100%;
}

.span-list {
  display: flex;
  flex-direction: column;
  position: absolute;
  z-index: 2;
  width: 100%;
}

.root,
.span {
  display: flex;
  align-items: center;
  height: 42px;
  justify-content: space-between;
}

.span {
  margin-top: 10px;
}

.dot {
  border-radius: 100%;
  margin-right: 10px;
}

.root .dot {
  width: 6px;
  height: 6px;
  background-color: #000000;
}

.span-left {
  display: flex;
  align-items: center;
}

.span .dot {
  width: 8px;
  height: 8px;
}

.pillar {
  height: 4px;
  border-radius: 1px;
}

.image {
  margin-right: 10px;
}

.error {
  width: 6px;
  height: 6px;
  border-radius: 100%;
  background-color: #e54c17;
  margin: 0px 10px -5px -15px;
}
</style>
