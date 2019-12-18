RppStatus  
rppi_occlusion_u8_pln1_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  rppHandle_t rppHandle )
{ 
	occlusion_host(
			static_cast<Rpp8u *>(srcPtr1),
			 srcSize1,
			static_cast<Rpp8u *>(dstPtr),
            dstSize,
            x11, y11, x12, y12, x21, y21, x22, y22,
			RPPI_CHN_PLANAR, 1 
			);


	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln1_batchSS_host(RppPtr_t srcPtr ,RppiSize srcSize ,RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,   RppiSize dstSize ,Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12 rpp::deref(rppHandle), paramIndex++);
copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 1
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln1_batchSD_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(dstSize, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
		x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 1
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln1_batchDS_host(RppPtr_t srcPtr ,RppiSize *srcSize ,RppPtr_t dstPtr , RppiSize *dstSize, Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12 rpp::deref(rppHandle), paramIndex++);
copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 1
	);
    return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln1_batchDD_host(RppPtr_t srcPtr1 ,RppiSize *srcSize1, RppPtr_t srcPtr2, RppiSize *dstSize, RppPtr_t dstPtr , Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 1
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln3_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  rppHandle_t rppHandle )
{ 
	occlusion_host(
			static_cast<Rpp8u *>(srcPtr1),
			 srcSize1,
			static_cast<Rpp8u *>(dstPtr),
            dstSize,
            x11, y11, x12, y12, x21, y21, x22, y22,
			RPPI_CHN_PLANAR, 3 
			);


	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln3_batchSS_host(RppPtr_t srcPtr ,RppiSize srcSize ,RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,   RppiSize dstSize ,Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 3
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln3_batchSD_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(dstSize, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
		x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 3
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln3_batchDS_host(RppPtr_t srcPtr ,RppiSize *srcSize ,RppPtr_t dstPtr , RppiSize *dstSize, Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 3
	);
    return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pln3_batchDD_host(RppPtr_t srcPtr1 ,RppiSize *srcSize1, RppPtr_t srcPtr2, RppiSize *dstSize, RppPtr_t dstPtr , Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PLANAR, 3
	);

	return RPP_SUCCESS;
}


RppStatus  
rppi_occlusion_u8_pkd3_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  rppHandle_t rppHandle )
{ 
	occlusion_host(
			static_cast<Rpp8u *>(srcPtr1),
			 srcSize1,
			static_cast<Rpp8u *>(dstPtr),
            dstSize,
            x11, y11, x12, y12, x21, y21, x22, y22,
			RPPI_CHN_PACKED, 3 
			);


	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchSS_host(RppPtr_t srcPtr ,RppiSize srcSize ,RppPtr_t dstPtr , Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,   RppiSize dstSize ,Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PACKED, 3
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchSD_host(RppPtr_t srcPtr1 ,RppiSize srcSize1, RppPtr_t srcPtr2, RppiSize dstSize, RppPtr_t dstPtr ,Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    copy_host_dstSize(dstSize, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
		x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PACKED, 3
	);

	return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchDS_host(RppPtr_t srcPtr ,RppiSize *srcSize ,RppPtr_t dstPtr , RppiSize *dstSize, Rpp32u x11, Rpp32u y11, Rpp32u x12, Rpp32u y12, Rpp32u x21, Rpp32u y21, Rpp32u x22, Rpp32u y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));
    copy_param_uint (x11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y11, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x12, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y12 rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y21, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (x22, rpp::deref(rppHandle), paramIndex++);
    copy_param_uint (y22, rpp::deref(rppHandle), paramIndex++);

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[1].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[2].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[3].uintmem,
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr[4].uintmem,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PACKED, 3
	);
    return RPP_SUCCESS;
}

RppStatus  
rppi_occlusion_u8_pkd3_batchDD_host(RppPtr_t srcPtr1 ,RppiSize *srcSize1, RppPtr_t srcPtr2, RppiSize *dstSize, RppPtr_t dstPtr , Rpp32u *x11, Rpp32u *y11, Rpp32u *x12, Rpp32u *y12, Rpp32u *x21, Rpp32u *y21, Rpp32u *x22, Rpp32u *y22,  Rpp32u nbatchSize ,rppHandle_t rppHandle )
{ 
	Rpp32u paramIndex = 0;
	//copy_host_srcSize(srcSize1, rpp::deref(rppHandle));
    //copy_host_dstSize(srcSize1, rpp::deref(rppHandle));

	occlusion_host_batch<Rpp8u>(
		static_cast<Rpp8u*>(srcPtr1),
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize1,
		static_cast<Rpp8u*>(srcPtr2),
        rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
		rpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,
         static_cast<Rpp8u*>(dstPtr),
        x11, y11, x12, y12, x21, y21, x22, y22,
		rpp::deref(rppHandle).GetBatchSize(),
		RPPI_CHN_PACKED, 3
	);

	return RPP_SUCCESS;
}
