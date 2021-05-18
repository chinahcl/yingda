<template>
<div id="change_unit">
  <el-table :data="tableData" style="width: 100%;line-height: 40px;" :row-class-name="tableRowClassName">
    <el-table-column prop="unit_name" label="单位名称" width="180"></el-table-column>
    <el-table-column prop="unit_abb" label="单位简称" width="180"></el-table-column>
    <el-table-column prop="use" label="联系人"></el-table-column>
    <el-table-column prop="phone" label="联系电话"></el-table-column>
    <el-table-column prop="iphone" label="手机号"></el-table-column>
    <el-table-column prop="address" label="办公地址"></el-table-column>
    <el-table-column prop="address" label="修改">
      <template slot-scope="scope">
        <!-- <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button> -->
        <el-button @click="handleClick(scope.row)" type="primary" size="small">编辑</el-button>
      </template>
    </el-table-column>
  </el-table>
<!-- <Pagination v-bind:child-msg="pageparm" @callFather="callFather"></Pagination> -->
<el-dialog :visible.sync="editFormVisible" width="50%" @click="closeDialog('editForm')">
      <el-form label-width="120px" :model="editForm" ref="editForm">
        <el-row>
          <el-col :span="12">
            <el-form-item label="单位名称">
              <el-input size="small" v-model="editForm.unit_name" ></el-input>
            </el-form-item>
            <el-form-item label="单位简称">
              <el-input size="small" v-model="editForm.unit_abb"></el-input>
            </el-form-item>
            <el-form-item label="联系人">
              <el-input size="small" v-model="editForm.use"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号">
              <el-input size="small" v-model="editForm.iphone"></el-input>
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input size="small" v-model="editForm.phone"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="办公地址">
          <el-input size="small" v-model="editForm.address" auto-complete="off" placeholder="请输入办公地址"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit()">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

</div>
</template>

<script>
import { Message } from 'element-ui'
import { setTimeout } from 'timers'
import 'element-ui/lib/theme-chalk/index.css'
export default {
  name: 'query_unit',
  data () {
    return {
      tableData: [],
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      editFormVisible: false,
      editForm: {
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
    this.axios.get('/users/', {
    }).then((res) => {
      this.tableData = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    handleClick (row) {
      this.editFormVisible = true
      this.editForm.iphone = row.iphone
      this.editForm.phone = row.phone
      this.editForm.unit_abb = row.unit_abb
      this.editForm.unit_name = row.unit_name
      this.editForm.use = row.use
      this.editForm.address = row.address
      this.editForm.id = row.id
      this.editForm.uintstate = row.uintstate
      this.editForm.userxu = row.userxu
      console.log(row)
    },
    onSubmit () {
      console.log('确认修改')
      const data = this.editForm
      const id = this.editForm.id
      const name = this.name
      console.log(id)
      // const _this = this
      this.axios.post('/users/' + id, {
        data,
        name
      }).then((res) => {
        console.log(res.data.code)
        if (res.data.code === 1) {
        // _this.$router.push('/index_1/change_unit')
          Message.success('修改成功')
          setTimeout(() => { location.reload() }, 800)
        } else {
          Message.warning('手机号重复！')
        }
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
