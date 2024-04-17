<template>
  <div>
    <el-table v-loading="loading" :data="data" row-key="id"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }">
      <el-table-column label="Method" prop="operation_name" />
      <el-table-column label="Duration(ms)" prop="duration" width="200" />
      <el-table-column label="Service" prop="cmdb_id" width="150" />
    </el-table>
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
      selectedTraceId: ""

    };
  },
  mounted() {
    this.fetchList(this.id)
  },
  watch: {
    id(newVal) {
      console.log('new' + newVal)
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
    }
  }
};
</script>

<style></style>