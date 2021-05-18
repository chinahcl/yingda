<template>
<div>
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="robot_name" label="机器人名称" ></el-table-column>
    <el-table-column prop="robot_path" label="机器人地址" ></el-table-column>
    <el-table-column label="编辑">
      <template slot-scope="scope">
        <!-- <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button> -->
        <el-button @click="handleClick(scope.$index, scope.row, tableData)" type="primary" size="small">编辑</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog :visible.sync="editFormVisible" width="40%" @click="closeDialog('editForm')">
      <el-form label-width="85px" :model="editForm" ref="editForm">
        <el-row>
          <!-- <el-col :span="12"> -->
            <el-form-item label="机器人名称">
              <el-input size="small" v-model="editForm.robot_name" ></el-input>
            </el-form-item>
            <el-form-item label="机器人地址">
              <el-input size="small" v-model="editForm.robot_path"></el-input>
            </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit()">确认修改</el-button>
        </el-form-item>
          <!-- </el-col> -->
        </el-row>
      </el-form>
    </el-dialog>
</div>
</template>

<script>
import { Message } from 'element-ui'
export default {
  name: 'query_unit',
  // created () {
  //   // 获取分类列表
  //   this.open()
  //   this.newdata = []
  // },
  data () {
    return {
      tableData: [],
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      editFormVisible: false,
      editForm: {
        id: '',
        robot_name: '',
        robot_path: ''
      }
    }
  },
  created () {
    const id = localStorage.use_unit
    this.axios.get('/robotapi/' + id, {
    }).then((res) => {
      // if(res.data)
      // Message.success('登陆成功')
      this.tableData = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    handleClick (index, row, rows) {
      this.index = index
      this.rows = rows
      this.editFormVisible = true
      this.editForm.id = row.id
      this.editForm.robot_name = row.robot_name
      this.editForm.robot_path = row.robot_path
      console.log(row)
    },
    onSubmit () {
      console.log('确认修改')
      const data = this.editForm
      const id = this.editForm.id
      const name = this.name
      console.log(id)
      // const _this = this
      this.axios.post('/robotapi/' + id, {
        data,
        name
      }).then((res) => {
        console.log(res.data.code)
        if (res.data.code === 1) {
        // _this.$router.push('/index_1/change_unit')
          Message.success('修改成功')
          this.editFormVisible = false
          this.rows.splice(this.index, 1, res.data.data)
          // setTimeout(() => { location.reload() }, 800)
        } else {
          Message.warning('机器人名称重复！')
        }
      })
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      } else if (rowIndex === 5) {
        return 'warning-row'
      } else if (rowIndex === 7) {
        return 'success-row'
      } else if (rowIndex === 9) {
        return 'warning-row'
      } else if (rowIndex === 11) {
        return 'success-row'
      } else if (rowIndex === 13) {
        return 'warning-row'
      } else if (rowIndex === 15) {
        return 'success-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
/* .el-table__header tr,
.el-table__header th {
  padding: 0;
  height: 30px;
  line-height: 40px;
}
.el-table__body tr,
.el-table__body td {
  padding: 0;
  height: 30px;
  line-height: 30px;
} */
</style>
