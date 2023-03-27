#pragma once

#define JWT_DISABLE_PICOJSON
#include "../third_party/jwt.h"

#include <jsoncpp/json/reader.h>
#include <jsoncpp/json/writer.h>

/**
 * JWT-CPP не зависит от конкретной JSON библиотеки, а может кастомизироваться через traits в шаблонах
 * предпочтительной вариацией. При условии, что в ней есть сущности, необходимые для маппинга в traits.
 * Ниже адаптация JsonCpp для нее.
 */

namespace jwt::traits
{

struct jsoncpp_traits
{
	// type aliases
	using value_type = Json::Value;
	using string_type = std::string;
	using number_type = double;
	using integer_type = int64_t;
	using boolean_type = bool;

	class object_type : public Json::Value
	{
	public:
		using mapped_type = Json::Value;
		using key_type = std::string;
		using size_type = size_t;

		object_type() = default;
		object_type(const object_type&) = default;
		object_type(const Json::Value& obj)
			: Json::Value(obj)
		{
		}
		object_type(object_type&&) = default;
		object_type(const Json::Value&& obj)
			: Json::Value(obj)
		{
		}
		~object_type() = default;
		object_type& operator=(const object_type& obj) = default;
		object_type& operator=(object_type&& obj) noexcept = default;

		const mapped_type& at(const key_type& key) const { return this->operator[](key); }

		size_type count(const key_type& key) const { return CountKey(*this, key); }

		size_type CountKey(const Json::Value& val, const std::string& key) const
		{
			// TODO: arrays ?
			size_type count = 0;
			for (const auto& mem_name : val.getMemberNames())
			{
				if (val[mem_name].isObject())
				{
					count += CountKey(val[mem_name], key);
				}
				if (mem_name == key)
				{
					count++;
				}
			}

			return count;
		}
	};

	class array_type : public Json::Value
	{
	public:
		using value_type = Json::Value;

		array_type() = default;
		array_type(const array_type&) = default;
		array_type(const Json::Value& arr)
			: Json::Value(arr)
		{
		}
		array_type(array_type&&) = default;
		array_type(const Json::Value&& arr)
			: Json::Value(arr)
		{
		}
		~array_type() = default;
		array_type& operator=(const array_type& arr) = default;
		array_type& operator=(array_type&& arr) noexcept = default;
	};

	// translation between the implementation notion of type, to the jwt::json::type equivalent
	static jwt::json::type get_type(const Json::Value& val)
	{

		if (val.isObject())
		{
			return jwt::json::type::object;
		}
		else if (val.isArray())
		{
			return jwt::json::type::array;
		}
		else if (val.isString())
		{
			return jwt::json::type::string;
		}
		else if (val.isDouble())
		{
			return jwt::json::type::number;
		}
		else if (val.isInt64())
		{
			return jwt::json::type::integer;
		}
		else if (val.isBool())
		{
			return jwt::json::type::boolean;
		}

		throw std::logic_error("unknown json type");
	}

	// conversion from generic value to specific type
	static object_type as_object(const Json::Value& val)
	{
		if (!val.isObject())
		{
			throw std::bad_cast();
		}
		return val;
	}

	static array_type as_array(const Json::Value& val)
	{
		if (!val.isArray())
		{
			throw std::bad_cast();
		}
		return val;
	}

	static string_type as_string(const Json::Value& val)
	{
		if (!val.isString())
		{
			throw std::bad_cast();
		}
		return val.asString();
	}

	static number_type as_number(const Json::Value& val)
	{
		if (!val.isDouble())
		{
			throw std::bad_cast();
		}
		return val.asDouble();
	}

	static integer_type as_integer(const Json::Value& val)
	{
		if (!val.isInt64())
		{
			throw std::bad_cast();
		}
		return val.asInt64();
	}

	static boolean_type as_boolean(const Json::Value& val)
	{
		if (!val.isBool())
		{
			throw std::bad_cast();
		}
		return val.asBool();
	}

	// serialization and parsing
	static bool parse(Json::Value& val, const std::string& str)
	{
		if (!Json::Reader().parse(str, val) || val.isNull() || !(val.isObject() || val.isArray()))
		{
			return false;
		}
		return true;
	}

	static std::string serialize(const Json::Value& val) { return Json::FastWriter().write(val); }
};

} // namespace jwt::traits
