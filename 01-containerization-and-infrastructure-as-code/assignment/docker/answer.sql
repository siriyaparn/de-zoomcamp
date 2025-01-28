-- Question 3
SELECT count(*) 
FROM public.green_taxi_trips
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01') 
    AND trip_distance <= 1;

SELECT count(*) 
FROM public.green_taxi_trips
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01') 
    AND (trip_distance > 1 AND trip_distance <= 3);

SELECT count(*) 
FROM public.green_taxi_trips
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01') 
    AND (trip_distance > 3 AND trip_distance <= 7);

SELECT count(*) 
FROM public.green_taxi_trips
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01') 
    AND (trip_distance > 7 AND trip_distance <= 10);

SELECT count(*) 
FROM public.green_taxi_trips
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01') 
    AND trip_distance > 10;

-- Question 4
SELECT lpep_pickup_datetime AS day
FROM public.green_taxi_trips
ORDER BY trip_distance DESC
LIMIT 1;

-- Question 5
SELECT zone
FROM public.lookup_zone 
JOIN public.green_taxi_trips 
    ON public.lookup_zone.locationid = public.green_taxi_trips.pulocationid
WHERE 
    lpep_pickup_datetime >= '2019-10-18' 
    AND lpep_pickup_datetime < '2019-10-19'
GROUP BY zone
HAVING SUM(total_amount) > 13000;

-- Question 6
SELECT dro.zone
FROM public.green_taxi_trips t
JOIN public.lookup_zone pu 
    ON t.pulocationid = pu.locationid
JOIN public.lookup_zone dro 
    ON t.dolocationid = dro.locationid
WHERE 
    (lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01')
    AND pu.zone = 'East Harlem North'
GROUP BY dro.zone, tip_amount
ORDER BY tip_amount DESC
LIMIT 1;