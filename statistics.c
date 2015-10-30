#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include "statistics.h"

static int compare_double_p(const void *p, const void *q) {
	double pd = *(const double *)p;
	double qd = *(const double *)q;
	
	if (pd > qd) {
		return 1;
	} else if (pd < qd) {
		return -1;
	} else {
		return 0;
	}
}

double mean(double arr[], size_t arrlen) {
	// Check for invalid array length
	if (arrlen == 0) {
		errno = EINVAL;
		return 0.0;
	}

	unsigned int i;
	double m = 0.0;

	// Calculate the running mean by intermediate averaging avoiding overflow
	for (i = 0; i < arrlen; i++) {
		m += arr[i] / arrlen;
	}

	return m;
}

double median(double arr[], size_t arrlen) {
	// Check for invalid array length
	if (arrlen == 0) {
		errno = EINVAL;
		return 0.0;
	}

	// Sort the array, then if array length is odd the median is in middle of array
	// if array length is even then median is halfway between the two middle elements
	qsort(arr, arrlen, sizeof(double), compare_double_p);
	if (arrlen % 2 == 0) {
		return arr[arrlen/2-1] + arr[arrlen/2]/2 - arr[arrlen/2-1]/2;
	} else {
		return arr[arrlen/2];
	}
}

double mode(double arr[], size_t arrlen) {
	// Check for invalid array length
	if (arrlen == 0) {
		errno = EINVAL;
		return 0.0;
	}

	size_t i;
	double most_freq_num = arr[0];
	size_t max_freq = 1;
	double curr_num = arr[0];
	size_t curr_freq = 1;

	// Compute the mode by maintaining a current num/freq and overwriting max num/freq when larger
	for (i = 1; i < arrlen; i++) {
		if (curr_freq > max_freq) {
			most_freq_num = curr_num;
			max_freq = curr_freq;
		}

		if (arr[i] == curr_num) {
			curr_freq++;
		} else {
			curr_num = arr[i];
			curr_freq = 1;
		}
	}

	return most_freq_num;
}

double range(double arr[], size_t arrlen) {
	// Check for invalid array length
	if (arrlen == 0) {
		errno = EINVAL;
		return 0.0;
	}

	// Sort to get the largest and smallest element and calculate range
	qsort(arr, arrlen, sizeof(double), compare_double_p);
	double range = arr[arrlen-1] - arr[0];

	// Check for overflow on the range
	if (arr[arrlen-1] > 0 && arr[0] < 0 && range < 0) {
		errno = EOVERFLOW;
		return range;
	} else if (arr[arrlen-1] < 0 && arr[0] > 0 && range > 0) {
		errno = EOVERFLOW;
		return range;
	}

	return range;
}