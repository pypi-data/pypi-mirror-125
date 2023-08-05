__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

inline void sort(IMAGE_dst_PIXEL_TYPE array[], int array_size)
{
    IMAGE_dst_PIXEL_TYPE temp;
    for(int i = 0; i < array_size; i++) {
        int j;
        temp = array[i];
        for(j = i - 1; j >= 0 && temp < array[j]; j--) {
            array[j+1] = array[j];
        }
        array[j+1] = temp;
    }
}

inline IMAGE_dst_PIXEL_TYPE median(IMAGE_dst_PIXEL_TYPE array[], int array_size)
{
    sort(array, array_size);
    return array[array_size / 2];
}

__kernel void median_box_2d
(
  IMAGE_dst_TYPE dst,
  IMAGE_src_TYPE src,
  const int Nx,
  const int Ny
)
{
  const int i = get_global_id(0), j = get_global_id(1);
  const int2 coord = (int2){i,j};

  int array_size = Nx * Ny;
  IMAGE_dst_PIXEL_TYPE array[MAX_ARRAY_SIZE];

  const int4   e = (int4)  { (Nx-1)/2, (Ny-1)/2, 0, 0 };

  float aSquared = e.x * e.x;
  float bSquared = e.y * e.y;

  int count = 0;

  for (int x = -e.x; x <= e.x; x++) {
    for (int y = -e.y; y <= e.y; y++) {
      array[count] = (IMAGE_dst_PIXEL_TYPE)READ_src_IMAGE(src,sampler,coord+((int2){x,y})).x;
      count++;
    }
  }
  array_size = count;
  //copyBoxNeighborhoodToArray(src, array, coord, Nx, Ny);

  IMAGE_dst_PIXEL_TYPE res = median(array, array_size);
  WRITE_dst_IMAGE(dst, coord, res);
}


