RppStatus  
rppi_occlusion_u8_pkd3_gpu(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize srcSize2, RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  rppHandle_t rppHandle )
{ 
#ifdef OCL_COMPILE
	{
		occlusion_cl(
			static_cast<cl_mem>(srcPtr1),
			srcSize1,
			static_cast<cl_mem>(srcPtr2),
            srcSize2,
			static_cast<cl_mem>(dstPtr),
            x11, y11, x12, y12, x21, y21, x22, y22,
			RPPI_CHN_PACKED, 1 ,rpp::deref(rppHandle));
	}
#elif defined (HIP_COMPILE)
	{
		occlusion_hip(
			static_cast<Rpp8u *>(srcPtr1),
			srcSize1,
			static_cast<Rpp8u *>(srcPtr2),
            srcSize2,
			static_cast<cl_mem>(dstPtr),
            x11, y11, x12, y12, x21, y21, x22, y22,
			RPPI_CHN_PACKED, 1 ,rpp::deref(rppHandle));
	}
#endif //BACKEND

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchSS_gpu(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
   
	Rpp32u paramIndex = 0;
	copy_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_dstSize(dstSize, rpp::deref(rppHandle));
	copy_srcMaxSize (rpp::deref(rppHandle));
    copy_dstMaxSize (rpp::deref(rppHandle));
	get_srcBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    get_dstBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

#ifdef OCL_COMPILE
	{
		occlusion_cl_batch(
			static_cast<cl_mem>(srcPtr1),
			static_cast<cl_mem>(srcPtr2),
			static_cast<cl_mem>(dstPtr),           
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#elif defined (HIP_COMPILE)
	{
		occlusion_hip_batch(
			static_cast<Rpp8u*>(srcPtr1),
			static_cast<Rpp8u*>(srcPtr2),
			static_cast<Rpp8u*>(dstPtr),
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#endif //BACKEND

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchSD_gpu(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
   
	Rpp32u paramIndex = 0;
	copy_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_dstSize(dstSize, rpp::deref(rppHandle));
	copy_srcMaxSize (rpp::deref(rppHandle));
    copy_dstMaxSize (rpp::deref(rppHandle));
	get_srcBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    get_dstBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

#ifdef OCL_COMPILE
	{
		occlusion_cl_batch(
			static_cast<cl_mem>(srcPtr1),
			static_cast<cl_mem>(srcPtr2),
			static_cast<cl_mem>(dstPtr),           
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#elif defined (HIP_COMPILE)
	{
		occlusion_hip_batch(
			static_cast<Rpp8u*>(srcPtr1),
			static_cast<Rpp8u*>(srcPtr2),
			static_cast<Rpp8u*>(dstPtr),
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#endif //BACKEND

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchDS_gpu(RppPtr_t srcPtr1 ,RppiSize *srcSize1, RppPtr_t srcPtr2, RppiSize *dstSize, RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )   
{ 
   
	Rpp32u paramIndex = 0;
	copy_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_dstSize(dstSize, rpp::deref(rppHandle));
	copy_srcMaxSize (rpp::deref(rppHandle));
    copy_dstMaxSize (rpp::deref(rppHandle));
	get_srcBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    get_dstBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

#ifdef OCL_COMPILE
	{
		occlusion_cl_batch(
			static_cast<cl_mem>(srcPtr1),
			static_cast<cl_mem>(srcPtr2),
			static_cast<cl_mem>(dstPtr),           
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#elif defined (HIP_COMPILE)
	{
		occlusion_hip_batch(
			static_cast<Rpp8u*>(srcPtr1),
			static_cast<Rpp8u*>(srcPtr2),
			static_cast<Rpp8u*>(dstPtr),
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#endif //BACKEND

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchDD_gpu(RppPtr_t srcPtr1 ,RppiSize *srcSize1 ,RppPtr_t srcPtr2 ,RppiSize *dstSize ,RppPtr_t dstPtr ,Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22, Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
   
	Rpp32u paramIndex = 0;
	copy_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_dstSize(dstSize, rpp::deref(rppHandle));
	copy_srcMaxSize (rpp::deref(rppHandle));
    copy_dstMaxSize (rpp::deref(rppHandle));
	get_srcBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    get_dstBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PACKED);
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

#ifdef OCL_COMPILE
	{
		occlusion_cl_batch(
			static_cast<cl_mem>(srcPtr1),
			static_cast<cl_mem>(srcPtr2),
			static_cast<cl_mem>(dstPtr),           
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#elif defined (HIP_COMPILE)
	{
		occlusion_hip_batch(
			static_cast<Rpp8u*>(srcPtr1),
			static_cast<Rpp8u*>(srcPtr2),
			static_cast<Rpp8u*>(dstPtr),
			rpp::deref(rppHandle),
			RPPI_CHN_PACKED,  3
		);
	}
#endif //BACKEND

	return RPP_SUCCESS;
}
