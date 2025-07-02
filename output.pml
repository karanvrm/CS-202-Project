
byte arr[6];
byte n;

inline merge(left, mid, right) {
    byte n1 = mid - left + 1;
    byte n2 = right - mid;

    byte L[6], R[6];
    byte i = 0;
    do
    :: (i < n1) ->
        L[i] = arr[left + i];
        i++;
    :: else -> break;
    od;

    byte j = 0;
    do
    :: (j < n2) ->
        R[j] = arr[mid + 1 + j];
        j++;
    :: else -> break;
    od;

    i = 0;
    j = 0;
    byte k = left;

    do
    :: (i < n1 && j < n2) ->
        if
        :: (L[i] <= R[j]) ->
            arr[k] = L[i];
            i++;
        :: else ->
            arr[k] = R[j];
            j++;
        fi;
        k++;
    :: else -> break;
    od;

    do
    :: (i < n1) ->
        arr[k] = L[i];
        i++;
        k++;
    :: else -> break;
    od;

    do
    :: (j < n2) ->
        arr[k] = R[j];
        j++;
        k++;
    :: else -> break;
    od;
}

inline mergeSort() {
    byte curr_size = 1;
    do
    :: (curr_size <= n - 1) ->
        byte left_start = 0;
        do
        :: (left_start < n - 1) ->
            byte mid = left_start + curr_size - 1;
            byte right_end;
            if
            :: (left_start + 2 * curr_size - 1 < n - 1) ->
                right_end = left_start + 2 * curr_size - 1;
            :: else ->
                right_end = n - 1;
            fi;
            merge(left_start, mid, right_end);
            left_start = left_start + 2 * curr_size;
        :: else -> break;
        od;
        curr_size = 2 * curr_size;
    :: else -> break;
    od;
}

inline printArray() {
    byte i = 0;
    do
    :: (i < n) ->
        printf("%d ", arr[i]);
        i++;
    :: else -> break;
    od;
    printf("\n");
}

init {
    arr[0] = 12;
    arr[1] = 11;
    arr[2] = 13;
    arr[3] = 5;
    arr[4] = 6;
    arr[5] = 7;

    n = 6;

    printf("Given array is \n");
    printArray();

    mergeSort();

    printf("\nSorted array is \n");
    printArray();
}
