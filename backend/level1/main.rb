require 'json'
require 'date'

class Runner
  def initialize(input_file)
    data = JSON.parse(File.read(input_file))
    @cars = data['cars']
    @rentals = data['rentals'].map do |rental|
      Rental.new(
        rental['id'],
        @cars,
        rental['car_id'],
        rental['start_date'],
        rental['end_date'],
        rental['distance']
      )
    end
  end

  def to_json(*args)
    File.open('backend/level1/data/output.json', 'wb') do |file|
      file.write(JSON.pretty_generate(@rentals.map(&:json)), args)
    end
  end
end

class Rental
  def initialize(id, cars, car_id, start_date, end_date, distance)
    @id = id
    @car = cars.find { |car| car['id'] == car_id }
    @start_date = DateTime.parse start_date
    @end_date = DateTime.parse end_date
    @distance = distance
  end

  def duration
    @end_date - @start_date + 1
  end

  def price
    @car['price_per_day'] * duration + @car['price_per_km'] * @distance
  end

  def json
    { id: @id, price: price.to_i }
  end
end

input_file = 'backend/level1/data/input.json'
puts Runner.new(input_file).to_json

#done
