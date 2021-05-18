<template>
<div class="fa_piao_shi_bie">
  <!-- :action="doUpload"    :data="pppss"-->
  <el-row>
    <h2 style="color:#048782;font-size:30px">发票识别机器人</h2>
  <el-col :span="8"><div class="grid-content bg-purple">
    <el-upload
  accept=".zip"
  class="upload-demo"
  drag
  :action="doUpload"
  :data="pppss"
  :on-success="handleSuccess"
  multiple>
  <i class="el-icon-upload"></i>
  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
  <div class="el-upload__tip" slot="tip">只能上传zip文件</div>
</el-upload>
    </div></el-col>
  <el-col :span="16"><div class="grid-content bg-purple-light">
    <el-table
      :data="tableData"
      height="740"
      style="width: 100%"
      :default-sort ="{prop:'created_time',order:'descending'}">
      <el-table-column
        sortable
        prop= "created_time"
        label="日期"
        :sort-orders="['descending','ascending']"
        >
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        >
      </el-table-column>
      <el-table-column
        prop="w_name"
        label="文件名称"
        >
      </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
      </template>
    </el-table-column>
    </el-table>
    </div></el-col>
</el-row>

  <!-- <div class="table_x"> -->
<el-dialog :visible.sync="editFormVisible" width="50%" @click="closeDialog('editForm')">
      <el-form label-width="120px" :model="editForm" ref="editForm">
        <el-row>
          <el-col :span="12">
            <el-form-item label="日期">
              <el-input size="small" v-model="editForm.created_time" ></el-input>
            </el-form-item>
            <el-form-item label="姓名">
              <el-input size="small" v-model="editForm.name"></el-input>
            </el-form-item>
            <el-form-item label="文件名称">
              <el-input size="small" v-model="editForm.w_name"></el-input>
            </el-form-item>
            <!-- <el-form-item label="地址">
              <el-input size="small" v-model="editForm.file"></el-input>
            </el-form-item> -->
          </el-col>
          <el-col :span="12">
              <!-- <el-form-item label="日期"> -->
              <!-- <el-input size="small" v-model="editForm.created_time" ></el-input> -->
              <el-button type="info" round v-if="editForm.file_state === '1'" disabled>识别中请稍后...</el-button>
              <!-- <el-button type="info" round v-if="editForm.file_state === '2'" disabled>运行中</el-button> -->
              <el-button icon="el-icon-download" type="danger" round v-if="editForm.file_state === '2'" @click="rusult_robot(editForm)">查看结果</el-button>
            <!-- </el-form-item> -->
          </el-col>
        </el-row>
      </el-form>
    </el-dialog>
</div>
<!-- </div> -->
</template>

<script>
// import API_CONFIG from '../../../vue.config'
export default {
  name: 'fa_piao_shi_bie',
  data () {
    return {
      // file_state: '',
      editFormVisible: false,
      tableData: [{
        id: '',
        created_time: '',
        name: '',
        file: '',
        w_name: '',
        file_state: '',
        down_file: ''
      }],
      // file_state: '',
      pppss: {
        name: localStorage.yun_user.replace('"', '').replace('"', '')
      },
      doUpload: '../robotapi/fa_piao_shi_bie/' + localStorage.yun_user.replace('"', '').replace('"', ''),
      editForm: {
      }
    }
  },
  created () {
    this.axios.get('../robotapi/fa_piao_shi_bie/' + this.pppss.name, {
    }).then((res) => {
      // if(res.data)
      // Message.success('登陆成功')
      this.tableData = res.data.data
      // this.file_state = res.data.data.file_state
      console.log(res)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    downloadFile (url, options = {}) {
      return new Promise((resolve, reject) => {
        // console.log(`${url} 请求数据，参数=>`, JSON.stringify(options))
        // axios.defaults.headers['content-type'] = 'application/json;charset=UTF-8'
        this.axios({
          method: 'get',
          url: url, // 请求地址
          data: options, // 参数
          responseType: 'blob' // 表明返回服务器返回的数据类型
        }).then(
          response => {
            // console.log("下载响应",response)
            resolve(response.data)
            const blob = new Blob([response.data], {
              // type: 'application/vnd.ms-excel'
              type: 'application/octet-stream'
            })
            // console.log(blob)
            // let fileName = Date.parse(new Date()) + '.xlsx'
            // console.log(response.headers['content-disposition'])
            // 切割出文件名
            const fileNameEncode = response.headers['content-disposition'].split("filename*=utf-8''")[1]
            // console.log(fileNameEncode)
            // 解码
            const fileName = decodeURIComponent(fileNameEncode)
            // console.log('fileName', fileName)
            if (window.navigator.msSaveOrOpenBlob) {
              // console.log(2)
              navigator.msSaveBlob(blob, fileName)
            } else {
              // console.log(3)
              var link = document.createElement('a')
              link.href = window.URL.createObjectURL(blob)
              link.download = fileName
              link.click()
              // 释放内存
              window.URL.revokeObjectURL(link.href)
            }
          },
          err => {
            reject(err)
          }
        )
      })
    },
    // 下载文件
    rusult_robot (editForm) {
      const postUrl = '../robotapi/fa_piao_shi_bie_start/' + editForm.id
      this.downloadFile(postUrl)
    },
    start_robot (editForm) {
      const id = editForm.id
      const data = editForm
      console.log(id)
      this.axios.post('../robotapi/fa_piao_shi_bie_start/' + id, {
        data
      }).then((res) => {
        location.reload()
      })
    },
    handleSuccess () {
      console.log('111')
      location.reload()
    },
    handleClick (row) {
      this.editFormVisible = true
      this.editForm.created_time = row.created_time
      this.editForm.id = row.id
      this.editForm.name = row.name
      this.editForm.file = row.file
      this.editForm.w_name = row.w_name
      this.editForm.file_state = row.file_state
      this.editForm.down_file = row.down_file
      console.log(row)
      if (row.file_state === '1') {
        setTimeout(() => {
          location.reload()
        }, 3000)
      }
    }
  }
}
</script>

<style scoped>
.batch_add_unit {
  line-height:55px;
  position:absolute;left:300px;top:200px;
}
.table_x {
  line-height:55px;
  position:absolute;left:200%;top:0px;
}
.row-bg {
    background: red;
  }
</style>
