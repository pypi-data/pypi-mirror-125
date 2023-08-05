__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

__kernel void binary_not_3d(
    IMAGE_src1_TYPE  src1,
    IMAGE_dst_TYPE  dst
)
{
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  const int z = get_global_id(2);

  const int4 pos = (int4){x,y,z,0};

  IMAGE_dst_PIXEL_TYPE value1 = CONVERT_dst_PIXEL_TYPE(READ_src1_IMAGE(src1, sampler, pos).x);
  if ( value1 != 0) {
    value1 = 0;
  } else {
    value1 = 1;
  }
  WRITE_dst_IMAGE (dst, pos, value1);
}

