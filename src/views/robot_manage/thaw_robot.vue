<template>
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="robot_name" label="机器人名称" ></el-table-column>
    <el-table-column prop="robot_path" label="机器人地址" ></el-table-column>
    <el-table-column label="状态">
      <template slot-scope="scope">
            <el-button @click.native.prevent="handleClick(scope.$index, scope.row, tableData)" type="primary" size="small">解冻</el-button>
            <!-- <el-tag type="danger" effect="dark" v-if="scope.row.userxu==3">删除</el-tag> -->
        </template>
    </el-table-column>
  </el-table>
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
      name: localStorage.yun_user.replace('"', "'").replace('"', "'")
    }
  },
  created () {
    const id = localStorage.use_unit
    this.axios.get('/robotapi/jiedong/' + id, {
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
    // handDelete (index, row) {
    //   console.log(index, row)
    // },
    handleClick (index, row, rows) {
      // this.editFormVisible = true
      const id = row.id
      const data = 0
      const name = this.name
      console.log(row)
      // const _this=this
      this.$confirm('此操作将解冻该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.post('/robotapi/jiedong/' + id, {
          data,
          name
        }).then((res) => {
          console.log(res.data.code)
          if (res.data.code === 1) {
            // _this.$router.push('/index_1/change_unit')
            Message.success('解冻成功')
            // this.handDelete(index, row)
            rows.splice(index, 1)
            // setTimeout(() => { location.reload() }, 800)
          } else {
            Message.warning('解冻失败')
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消解冻'
        })
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
