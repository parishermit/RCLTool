<template>
    <div>
        <div style="display: flex;justify-content: space-between;align-items: center;">
            <div style="display: flex;">
                <div style="background-color: #007bff;width: 2px;margin-right: 5px;"></div>Task List
            </div>
            <button class="btn" @click="dialogFormVisible = true">New Task</button>
        </div>
        <div style="width: 100%;">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(task, index) in taskList" :key="index">
                        <td>{{ task.id }}</td>
                        <td>{{ task.name }}</td>
                        <td>{{ task.status }}</td>
                        <td>{{ task.progress }}</td>
                    </tr>
                </tbody>
            </table>
            <el-pagination background layout="prev, pager, next" :total="1000">
            </el-pagination>
            <el-dialog title="New Task" :visible.sync="dialogFormVisible">
                <el-form :model="form" size="mini">
                    <el-form-item label="Task Name" :label-width="formLabelWidth" label-suffix="1">
                        <el-input v-model="form.Taskname" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Upload" :label-width="formLabelWidth">
                        <el-upload class="upload-demo" style="text-align: left;"
                        :action="'http://localhost:8000/upload?file_name=' + form.Taskname"
                        >
                            <div>
                                <el-button size="mini" icon="el-icon-upload2">upload</el-button>
                            </div>
                        </el-upload>
                    </el-form-item>
                    <div style="margin: 5px 0;text-align: left;font-size: 18px;font-weight: bold;">Parameters</div>
                    <el-form-item label="Learning Rate" :label-width="formLabelWidth">
                        <el-input v-model="form.LearningRate" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Batchsize" :label-width="formLabelWidth">
                        <el-input v-model="form.Batchsize" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Epoch" :label-width="formLabelWidth">
                        <el-input v-model="form.Epoch" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="NumberOfLabels" :label-width="formLabelWidth">
                        <el-input v-model="form.NumberOfLabels" autocomplete="off"></el-input>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false" size="mini" round>cancel</el-button>
                    <el-button type="primary" @click="submitForm" size="mini" round>start</el-button>
                </div>
            </el-dialog>
        </div>

    </div>
</template>

<script>
import { saveTask, getTask } from '@/api/trace.js'
export default {
    name: 'Task',
    data() {
        return {
            taskList: [],
            currentPage: 1,
            pageSize: 5, // 每页显示5条数据
            dialogFormVisible: false,
            dialogWidth: '100px',
            form: {
                TaskName: '',
                LearningRate: '0.0001',
                Batchsize: '32',
                Epoch: '15',
                NumberOfLabels: '35'
            },
            formLabelWidth: '120px'
        };
    },
    mounted() {
        // 组件挂载时，发送请求获取任务列表数据
        this.fetchTaskList();
    },
    computed: {

    },

    methods: {
        // 提交表单
        submitForm() {
            saveTask({
                form: this.form
            }).then((res) => {
                this.fetchTaskList()
                this.dialogFormVisible = false
            })
        },

        // 获取任务列表数据
        fetchTaskList() {
            getTask({}).then((res) => {
                this.taskList = res.data.taskList
                console.log(this.taskList)
            })

        }
    }
};
</script>

<style scoped>
/* 添加页面样式 */
table {
    width: 100%;
    /* 设置表格宽度为100% */
    border-collapse: collapse;
}

th,
td {
    padding: 8px;
    text-align: left;
}

th {
    background-color: rgb(245, 248, 250);
}

/* 实现斑马条纹效果 */
tr:nth-child(even) {
    background-color: rgb(245, 248, 250);
}

.btn {
    background-color: #007bff;
    /* 蓝色背景 */
    border: none;
    /* 移除边框 */
    color: white;
    /* 白色字体 */
    padding: 10px 20px;
    /* 按钮内边距 */
    text-align: center;
    /* 文字居中 */
    text-decoration: none;
    /* 移除下划线 */
    display: inline-block;
    /* 行内块元素 */
    font-size: 16px;
    /* 字体大小 */
    border-radius: 20px;
    /* 圆角 */
    cursor: pointer;
    /* 鼠标指针样式 */
}
</style>