<template>
  <div class="custom-tree-container">

    <!-- <el-tree
      :data="data"
      node-key="id"
      default-expand-all
      :expand-on-click-node="false">
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <span>
          <el-button
            type="text"
            size="mini"
            @click="() => append(data)">
            Append
          </el-button>
          <el-button
            type="text"
            size="mini"
            @click="() => remove(node, data)">
            Delete
          </el-button>
        </span>
      </span>
    </el-tree> -->



    <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick" default-expand-all >

      <span class="custom-tree-node" slot-scope="{ node, data }">
        <el-tooltip content="extra info" placement="top">
          <div>

            <div class="bar" :style="'width:' + data.length * 900 + 'px'">{{ data.duration }}ms</div>

            <div class="node-label">{{ data.cmdb_id }}&nbsp; &nbsp;&nbsp;&nbsp;{{ node.label }}</div>
          </div>
        </el-tooltip>
      </span>

    </el-tree>
  </div>
</template>

<script>
import { getTree } from '@/api/trace.js'
export default {
  props: {
    id: String,
  },
  data() {
    return {
      data: [],
      selectedTraceId: "",
      defaultProps: {
        children: 'children',
        label: 'operation_name',
      }
    };
  },
  mounted() {
    this.fetchList(this.id)
  },
  watch: {
    id(newVal) {
      console.log('new' + newVal)
      console.log("AAA/")
      console.log(this.data)
      this.selectedTraceId = newVal;
      this.fetchList(newVal)
    }
  },
  methods: {
    handleNodeClick(data) {
      console.log(data);
    },
    fetchList(Id) {
      getTree({ trace_id: Id }).then((ans) => {
        this.data = ans.data
        console.log(this.data)
      })
    },
        // getColor(label) {
    //   if (label === 'frontend2-0') {
    //     return '#57CF95';
    //   } else if (label === '2') {
    //     return 'yellow';
    //   } else if (label === '3') {
    //     return 'green';
    //   } else {
    //     return '#ddd'; // 默认
    //   }
    // },
  }
};
</script>
<style>
.progress-bar {
  height: 5px;
  background-color: #ddd;
  border-radius: 5px;
}

.el-tree-node__content {
  height: 80px;
}

.bar {
  background-color: #57CF95;
}

.node-label {
  text-align: left;
}
</style>