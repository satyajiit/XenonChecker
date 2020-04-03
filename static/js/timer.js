function runTimer(){


             distance-=1000;
             console.log(distance)

            // Time calculations for days, hours, minutes and seconds
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            $('#timerData').text(
                minutes + "m " + seconds + "s ");
            $('#progressBar').css("width", ((maxTime-distance)*100/maxTime)+"%")

            // If the count down is finished, write some text
            if (distance < 0) {
                clearInterval(time)
                    $('#timerData').text("Time Expired");
                sendAnswer();
            }
        }

