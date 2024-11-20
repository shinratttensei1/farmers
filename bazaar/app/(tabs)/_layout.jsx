import { View, Text, Image, ImageSourcePropType } from 'react-native'
import { Tabs, Redirect } from 'expo-router'
import "../global.css"

import { icons } from '../../constants'

const TabIcon = ({ icon, color, name, focused }) => {
    return (
        <View className='items-center justify-bottom gap-2'>
          <Image
          source={icon}
          tintColor={color}
          style={{
            resizeMode: 'center',
            width: 30,
            height: 30,
          }}
          />
            <Text className={`${focused ? 'font-psemibold' : 'font-pregular'} text-xs text-zinc`}>
              {name}
            </Text>
        </View>
    )
}

const TabsLayout = () => {
  return (
    <>
      <Tabs
        screenOptions={{
          tabBarActiveTintColor: "#FFA001",
          tabBarInactiveTintColor: "#CDCDE0",
          tabBarShowLabel: false,
          tabBarStyle: {
            backgroundColor: "#161622",
            borderTopWidth: 1,
            borderTopColor: "#232533",
            height: 84,
        },
      }}
      >
        <Tabs.Screen
          name="crops"
          options={{
            title: 'Crops',
            headerShown: false,
            tabBarIcon: ({ color, focused }) => (
              <TabIcon
                  icon={icons.crops}
                  color={color}
                  name="Crops"
                  focused={focused}
              />
            )
          }}
        />
                <Tabs.Screen
          name="profile"
          options={{
            title: 'Profile',
            headerShown: false,
            tabBarIcon: ({ color, focused }) => (
              <TabIcon
                  icon={icons.profile}
                  color={color}
                  name="Profile"
                  focused={focused}
              />
            )
          }}
        />
      </Tabs>
    </>
  )
}

export default TabsLayout