<template>
<div id="change_unit">
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="unit_index" label="序列" width="80"></el-table-column>
    <el-table-column prop="unit_name" label="单位名称" width="180"></el-table-column>
    <el-table-column prop="unit_abb" label="单位简称" width="180"></el-table-column>
    <el-table-column prop="use" label="联系人"></el-table-column>
    <el-table-column prop="phone" label="联系电话"></el-table-column>
    <el-table-column prop="iphone" label="手机号"></el-table-column>
    <el-table-column prop="address" label="办公地址"></el-table-column>
    <el-table-column prop="address" label="状态">
      <template slot-scope="scope">
        <!-- <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button> -->
        <el-button @click="handleClick(scope.$index, scope.row, tableData)" type="primary" size="small">冻结</el-button>
      </template>
    </el-table-column>
  </el-table>
</div>
</template>

<script>
import { Message } from 'element-ui'
// import { setTimeout } from 'timers'
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
      editForm: {
        unit_index: '',
        id: '',
        iphone: '',
        phone: '',
        unit_abb: '',
        unit_name: '',
        use: '',
        address: '',
        uintstate: '',
        userxu: ''
      }
    }
  },
  created () {
    this.axios.get('/users/zhengchang', {
    }).then((res) => {
      this.tableData = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    handleClick (index, row, rows) {
      // this.editFormVisible = true
      const id = row.id
      const data = 2
      const name = localStorage.yun_user.replace('"', '').replace('"', '')
      console.log(row)
      // const _this=this
      this.$confirm('此操作将冻结该公司, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.axios.post('/users/zhengchang/' + id, {
          data,
          name
        }).then((res) => {
          console.log(res.data.code)
          if (res.data.code === 1) {
            // _this.$router.push('/index_1/change_unit')
            Message.success('冻结成功')
            rows.splice(index, 1)
            // setTimeout(() => { location.reload() }, 800)
          } else {
            Message.warning('冻结失败')
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消冻结'
        })
      })
    }
    // tableRowClassName ({ row, rowIndex }) {
    //   if (rowIndex === 1) {
    //     return 'warning-row'
    //   } else if (rowIndex === 3) {
    //     return 'success-row'
    //   } else if (rowIndex === 5) {
    //     return 'warning-row'
    //   } else if (rowIndex === 7) {
    //     return 'success-row'
    //   } else if (rowIndex === 9) {
    //     return 'warning-row'
    //   } else if (rowIndex === 11) {
    //     return 'success-row'
    //   } else if (rowIndex === 13) {
    //     return 'warning-row'
    //   } else if (rowIndex === 15) {
    //     return 'success-row'
    //   }
    //   return ''
    // }
  }
}
</script>

<style scoped>
.el-table >>> .warning-row {
  background: oldlace;
}

.el-table >>> .success-row {
  background: #f0f9eb;
}
</style>
