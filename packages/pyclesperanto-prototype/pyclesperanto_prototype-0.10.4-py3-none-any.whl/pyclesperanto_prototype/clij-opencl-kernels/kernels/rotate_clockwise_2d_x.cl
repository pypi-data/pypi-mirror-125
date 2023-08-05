__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;


__kernel void rotate_right_2d(
    IMAGE_dst_TYPE dst,
    IMAGE_src_TYPE src
) {
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

  const int sx = get_global_id(1);
  const int sy = get_global_size(0) - get_global_id(0) - 1;

  const int dx = get_global_id(0);
  const int dy = get_global_id(1);

  const IMAGE_src_PIXEL_TYPE out = READ_src_IMAGE(src,sampler,(int2)(sx,sy)).x;
  WRITE_dst_IMAGE(dst,(int2)(dx,dy), CONVERT_dst_PIXEL_TYPE(out));
}
